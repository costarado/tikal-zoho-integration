"""
Zoho → Tikal call service (Production)
- POST /api/call/create  : originate call in Tikal
- GET  /dial             : UI page for click-to-call from Zoho (select phone + agent_id)
- GET  /health           : service health
- GET  /api/call/status  : tikal connectivity check (light)

ENV (Railway Variables):
TIKAL_BASE_URL
TIKAL_API_KEY
TIKAL_FORMAT (optional, default json)

ZOHO_ACCOUNTS_DOMAIN (default https://accounts.zoho.com)
ZOHO_API_DOMAIN      (default https://www.zohoapis.com)
ZOHO_CLIENT_ID
ZOHO_CLIENT_SECRET
ZOHO_REFRESH_TOKEN
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import sys
import io
import logging
import time
import re
import requests

# --- stdout utf-8 (keep from your version) ---
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    from tikal_client.tikal_client_v2 import TikalClientV2
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    sys.exit(1)

app = Flask(__name__)
CORS(app)  # ok: service + /dial are same origin on Railway

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------
# TIKAL config (from env)
# -----------------------------
TIKAL_BASE_URL = os.environ.get("TIKAL_BASE_URL", "http://arielsip.com")
TIKAL_API_KEY = os.environ.get("TIKAL_API_KEY")  # REQUIRED in prod
TIKAL_FORMAT = os.environ.get("TIKAL_FORMAT", "json")

# -----------------------------
# ZOHO config (from env)
# -----------------------------
ZOHO_ACCOUNTS_DOMAIN = os.environ.get("ZOHO_ACCOUNTS_DOMAIN", "https://accounts.zoho.com")
ZOHO_API_DOMAIN = os.environ.get("ZOHO_API_DOMAIN", "https://www.zohoapis.com")
ZOHO_CLIENT_ID = os.environ.get("ZOHO_CLIENT_ID")
ZOHO_CLIENT_SECRET = os.environ.get("ZOHO_CLIENT_SECRET")
ZOHO_REFRESH_TOKEN = os.environ.get("ZOHO_REFRESH_TOKEN")

# -----------------------------
# Zoho modules / fields (фиксируем по твоим данным)
# -----------------------------
ALLOWED_MODULES = {"Contacts", "Deals", "Sales_Orders"}

# Deals.Contact_Name lookup → contact id
# Sales_Orders.Contact_Name lookup → contact id
CONTACT_LOOKUP_FIELD = "Contact_Name"

PHONE_FIELDS = [
    ("Mobile", "Mobile"),
    ("Phone", "Phone"),
    ("Other Phone", "Other_Phone"),
    ("Home Phone", "Home_Phone"),
    ("Asst Phone", "Asst_Phone"),
    ("Phone 2 (raw)", "Phone_2_raw"),
]

# -----------------------------
# Helpers
# -----------------------------
def create_tikal_client() -> TikalClientV2:
    if not TIKAL_API_KEY:
        raise RuntimeError("TIKAL_API_KEY is missing (set Railway Variable)")
    return TikalClientV2(base_url=TIKAL_BASE_URL, api_key=TIKAL_API_KEY, format=TIKAL_FORMAT)


def _digits(s: str) -> str:
    return re.sub(r"\D+", "", s or "")


def _normalize_phone_for_tikal(raw: str) -> str:
    """
    Минимальная нормализация: оставить только цифры.
    Если нужно E.164/CallerID — расширим позже.
    """
    return _digits(raw)


# -----------------------------
# Zoho OAuth token cache
# -----------------------------
_token_cache = {"token": None, "exp": 0}


def _zoho_env_ok() -> bool:
    return all([ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET, ZOHO_REFRESH_TOKEN, ZOHO_API_DOMAIN, ZOHO_ACCOUNTS_DOMAIN])


def _get_zoho_access_token() -> str:
    """
    Uses refresh_token to get access_token.
    Caches access token in-memory.
    """
    if not _zoho_env_ok():
        raise RuntimeError("Zoho OAuth env vars are missing (ZOHO_CLIENT_ID/SECRET/REFRESH_TOKEN/API_DOMAIN/ACCOUNTS_DOMAIN)")

    now = time.time()
    if _token_cache["token"] and now < (_token_cache["exp"] - 60):
        return _token_cache["token"]

    url = f"{ZOHO_ACCOUNTS_DOMAIN}/oauth/v2/token"
    resp = requests.post(
        url,
        data={
            "grant_type": "refresh_token",
            "client_id": ZOHO_CLIENT_ID,
            "client_secret": ZOHO_CLIENT_SECRET,
            "refresh_token": ZOHO_REFRESH_TOKEN,
        },
        timeout=20,
    )
    # Zoho returns 200 with json or error codes
    resp.raise_for_status()
    data = resp.json()

    token = data.get("access_token")
    if not token:
        raise RuntimeError(f"Failed to refresh Zoho access token: {data}")

    expires_in = int(data.get("expires_in", 3600))
    _token_cache["token"] = token
    _token_cache["exp"] = now + expires_in
    return token


def _zoho_get_record(module_api_name: str, record_id: str, fields=None) -> dict:
    """
    GET /crm/v2/{module}/{id}?fields=...
    """
    token = _get_zoho_access_token()
    url = f"{ZOHO_API_DOMAIN}/crm/v2/{module_api_name}/{record_id}"

    params = {}
    if fields:
        params["fields"] = ",".join(fields)

    resp = requests.get(
        url,
        headers={"Authorization": f"Zoho-oauthtoken {token}"},
        params=params,
        timeout=20,
    )

    # If Zoho returns error body, surface it cleanly
    if resp.status_code >= 400:
        try:
            body = resp.json()
        except Exception:
            body = {"raw": resp.text}
        raise RuntimeError(f"Zoho API error {resp.status_code}: {body}")

    payload = resp.json()
    rec = (payload.get("data") or [None])[0] or {}
    return rec


# -----------------------------
# UI: /dial page (Zoho button opens this)
# -----------------------------
DIAL_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Call (Tikal)</title>
  <style>
    body{font-family:Arial, sans-serif; margin:20px; max-width:780px;}
    .box{padding:12px; border:1px solid #ddd; border-radius:8px; margin:12px 0;}
    label{display:block; margin:6px 0;}
    input[type=text]{padding:8px; width:240px;}
    button{padding:10px 14px; cursor:pointer;}
    pre{background:#111; color:#0f0; padding:12px; border-radius:8px; overflow:auto;}
    .err{color:#b00;}
    .muted{color:#666; font-size: 13px;}
  </style>
</head>
<body>
  <h2>Call via Tikal</h2>

  {% if error %}
    <div class="box">
      <div class="err"><b>Error:</b> {{error}}</div>
      <div class="muted" style="margin-top:8px;">
        Проверь: (1) Railway Variables ZOHO_* (2) правильный module/recordId в кнопке Zoho (3) связь Contact_Name заполнена.
      </div>
    </div>
  {% else %}
    <div class="box">
      <div><b>Source:</b> {{source_module}} / {{source_record_id}}</div>
      <div><b>Contact:</b> {{contact_name}} ({{contact_id}})</div>
    </div>

    <div class="box">
      <label><b>Agent ID (extension)</b><br/>
        <input id="agentId" type="text" placeholder="e.g. 101"/>
      </label>

      <div style="margin-top:10px;"><b>Select phone</b></div>
      {% if phones %}
        {% for p in phones %}
          <label>
            <input type="radio" name="phone" value="{{p['value']}}" {% if loop.first %}checked{% endif %}/>
            {{p['label']}}: {{p['value']}}
          </label>
        {% endfor %}
      {% else %}
        <div class="err">No phone numbers found on this contact.</div>
      {% endif %}

      <div style="margin-top:12px;">
        <button id="callBtn" {% if not phones %}disabled{% endif %}>Call</button>
      </div>

      <div class="muted" style="margin-top:10px;">
        Agent ID запоминается в браузере (на этом компьютере).
      </div>
    </div>

    <div class="box">
      <div><b>Result</b></div>
      <pre id="out">{}</pre>
    </div>
  {% endif %}

<script>
  const agent = document.getElementById('agentId');
  if (agent) {
    agent.value = localStorage.getItem('tikal_agent_id') || '';
    agent.addEventListener('input', () => localStorage.setItem('tikal_agent_id', agent.value));
  }

  const callBtn = document.getElementById('callBtn');
  if (callBtn) {
    callBtn.addEventListener('click', async () => {
      const agentId = (agent.value || '').trim();
      if (!agentId) { alert('Agent ID is required'); return; }

      const chosen = document.querySelector('input[name="phone"]:checked');
      if (!chosen) { alert('Choose phone'); return; }

      const payload = {
        agent_id: agentId,
        phone_number: chosen.value,
        zoho_contact_id: "{{contact_id}}",
        custom2: "{{source_module}}:{{source_record_id}}"
      };

      const out = document.getElementById('out');
      out.textContent = 'Calling...';

      try {
        const r = await fetch('/api/call/create', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(payload)
        });
        const data = await r.json().catch(() => ({}));
        out.textContent = JSON.stringify({status: r.status, ...data}, null, 2);
      } catch (e) {
        out.textContent = String(e);
      }
    });
  }
</script>
</body>
</html>
"""


@app.route("/dial", methods=["GET"])
def dial_page():
    """
    Opens UI for click-to-call.
    Expects:
      /dial?module=Contacts|Deals|Sales_Orders&recordId=<zoho_record_id>
    """
    source_module = (request.args.get("module") or "").strip()
    source_record_id = (request.args.get("recordId") or "").strip()

    if source_module not in ALLOWED_MODULES:
        return render_template_string(DIAL_HTML, error=f"Bad module '{source_module}'. Allowed: {sorted(ALLOWED_MODULES)}"), 400
    if not source_record_id:
        return render_template_string(DIAL_HTML, error="Missing recordId"), 400

    try:
        # resolve contact_id
        if source_module == "Contacts":
            contact_id = source_record_id
        else:
            rec = _zoho_get_record(source_module, source_record_id, fields=[CONTACT_LOOKUP_FIELD])
            lk = rec.get(CONTACT_LOOKUP_FIELD)
            contact_id = (lk or {}).get("id") if isinstance(lk, dict) else None

        if not contact_id:
            return render_template_string(
                DIAL_HTML,
                error=f"No linked contact found in {source_module}.{CONTACT_LOOKUP_FIELD} for record {source_record_id}",
            ), 400

        # load contact phones + name
        fields = [f for _, f in PHONE_FIELDS] + ["Full_Name", "First_Name", "Last_Name"]
        c = _zoho_get_record("Contacts", contact_id, fields=fields)

        contact_name = (c.get("Full_Name") or "").strip()
        if not contact_name:
            first = (c.get("First_Name") or "").strip()
            last = (c.get("Last_Name") or "").strip()
            contact_name = (first + " " + last).strip() or "Contact"

        phones = []
        seen = set()
        for label, api_name in PHONE_FIELDS:
            raw_val = c.get(api_name)
            if not raw_val:
                continue
            raw_str = str(raw_val).strip()
            dig = _digits(raw_str)
            if len(dig) < 5:
                continue
            if dig in seen:
                continue
            seen.add(dig)
            phones.append({"label": label, "value": raw_str})

        return render_template_string(
            DIAL_HTML,
            error=None,
            source_module=source_module,
            source_record_id=source_record_id,
            contact_id=contact_id,
            contact_name=contact_name,
            phones=phones,
        )

    except Exception as e:
        logger.error(f"/dial error: {e}", exc_info=True)
        return render_template_string(DIAL_HTML, error=str(e)), 500


# -----------------------------
# Health / status
# -----------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "ok",
            "service": "Zoho Call Service",
            "tikal_api": TIKAL_BASE_URL,
            "environment": os.environ.get("ENVIRONMENT", "production"),
            "zoho_api_domain": ZOHO_API_DOMAIN,
        }
    )


@app.route("/api/call/status", methods=["GET"])
def call_status():
    try:
        client = create_tikal_client()
        client.close()
        return jsonify(
            {
                "status": "ok",
                "tikal_api": TIKAL_BASE_URL,
                "service": "Zoho Call Service",
                "environment": os.environ.get("ENVIRONMENT", "production"),
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


# -----------------------------
# Call create (Zoho -> this -> Tikal)
# -----------------------------
@app.route("/api/call/create", methods=["POST"])
def create_call():
    """
    JSON:
    - agent_id (required) -> Tikal: agent_id
    - phone_number (required) -> Tikal: dest_num
    - custom1 (optional)
    - custom2 (optional)
    - zoho_contact_id (optional) -> if custom1 empty, goes to custom1
    """
    client = None
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"success": False, "error": "No JSON data provided"}), 400

        agent_id = data.get("agent_id")
        phone_number = data.get("phone_number") or data.get("dest_num")

        if not agent_id:
            return jsonify({"success": False, "error": "agent_id is required"}), 400

        if not phone_number:
            return jsonify({"success": False, "error": "phone_number is required"}), 400

        custom1 = data.get("custom1", "") or ""
        custom2 = data.get("custom2", "") or ""
        zoho_contact_id = data.get("zoho_contact_id", "") or ""

        # normalize phone for Tikal
        phone_number_norm = _normalize_phone_for_tikal(str(phone_number))
        if not phone_number_norm:
            return jsonify({"success": False, "error": "phone_number is invalid after normalization"}), 400

        client = create_tikal_client()

        logger.info(f"Creating call: agent_id={agent_id}, phone={phone_number_norm}")

        result = client.calls.originate(
            agent_id=str(agent_id),
            dest_num=phone_number_norm,
            custom1=custom1 or zoho_contact_id,
            custom2=custom2,
        )

        # success check (same logic as your version)
        if result.get("data", {}).get("status", {}).get("code") == "200":
            return jsonify(
                {
                    "success": True,
                    "message": "Call created successfully",
                    "data": result.get("data", {}),
                    "agent_id": str(agent_id),
                    "phone_number": phone_number_norm,
                }
            ), 200

        error_msg = result.get("data", {}).get("status", {}).get("message", "Unknown error")
        return jsonify({"success": False, "error": error_msg, "data": result}), 400

    except Exception as e:
        logger.error(f"Error creating call: {e}", exc_info=True)
        return jsonify({"success": False, "error": str(e)}), 500

    finally:
        try:
            if client:
                client.close()
        except Exception:
            pass


# -----------------------------
# Local run (Railway typically runs via gunicorn)
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("=" * 70)
    print("📞 Zoho Call Service - Production Version")
    print("=" * 70)
    print(f"\n🌐 Service port: {port}")
    print("📋 Endpoints:")
    print("   GET  /health")
    print("   GET  /dial?module=Contacts|Deals|Sales_Orders&recordId=<id>")
    print("   POST /api/call/create")
    print("   GET  /api/call/status")
    print("=" * 70)
    app.run(host="0.0.0.0", port=port, debug=False)
