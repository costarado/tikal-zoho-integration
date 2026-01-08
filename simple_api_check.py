"""
Simple API endpoint checker
Checks common API paths without encoding issues
"""

import requests
import sys
from config import TIKAL_CONFIG

def check_api_paths():
    """Checks common API paths"""
    base_url = TIKAL_CONFIG['base_url'].rstrip('/')
    access_token = TIKAL_CONFIG.get('access_token', '')
    
    print("=" * 70)
    print("Simple API Endpoint Checker")
    print("=" * 70)
    print(f"\nBase URL: {base_url}")
    print(f"Token: {'Set' if access_token else 'Not set'}\n")
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Common API paths to check
    paths = [
        # Direct API paths
        '/cc3/api',
        '/cc3/api/',
        '/cc3/api/agents',
        '/cc3/api/calls',
        '/cc3/api/recordings',
        '/cc3/api/statistics',
        
        # REST paths
        '/cc3/rest',
        '/cc3/rest/',
        '/cc3/rest/agents',
        '/cc3/rest/calls',
        
        # Through index.php with format=json
        '/cc3/index.php?format=json&action=agents',
        '/cc3/index.php?format=json&cat=agents',
        '/cc3/index.php?api=1&action=agents',
        '/cc3/index.php?output=json&action=agents',
        
        # API files
        '/cc3/api.php',
        '/cc3/api/index.php',
        '/cc3/api/agents.php',
        '/cc3/api/calls.php',
        '/cc3/rest.php',
        
        # Standard REST
        '/api',
        '/api/agents',
        '/api/calls',
        '/api/v1/agents',
        '/api/v1/calls',
    ]
    
    print("Checking API paths...\n")
    print("-" * 70)
    
    found = []
    
    for path in paths:
        url = f"{base_url}{path}"
        try:
            response = requests.get(url, headers=headers, timeout=5, verify=False)
            content_type = response.headers.get('Content-Type', '').lower()
            
            # Check if it's JSON
            is_json = 'json' in content_type
            try:
                json_data = response.json()
                is_json = True
            except:
                json_data = None
            
            if response.status_code != 404:
                status_icon = "OK" if response.status_code == 200 else "?"
                print(f"{status_icon} {response.status_code:3d} | {path}")
                
                if is_json or json_data:
                    print(f"     -> JSON response found!")
                    if json_data:
                        keys = list(json_data.keys())[:5]
                        print(f"     -> Keys: {keys}")
                    found.append({'path': path, 'url': url, 'status': response.status_code})
                elif response.status_code == 200:
                    text_preview = response.text[:100].replace('\n', ' ')
                    if 'api' in text_preview.lower() or 'json' in text_preview.lower():
                        print(f"     -> Possible API endpoint")
                        found.append({'path': path, 'url': url, 'status': response.status_code})
        except Exception as e:
            pass
    
    print("\n" + "=" * 70)
    if found:
        print(f"Found {len(found)} potential API endpoints:\n")
        for item in found:
            print(f"  {item['status']} - {item['path']}")
        print("\nUpdate config.py with these paths")
    else:
        print("No API endpoints found")
        print("\nNext steps:")
        print("1. Check PDF documentation manually")
        print("2. Check web interface settings/configuration")
        print("3. Contact Tikal support for API documentation")
        print("4. Check if API needs to be enabled in admin panel")


if __name__ == '__main__':
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    check_api_paths()

