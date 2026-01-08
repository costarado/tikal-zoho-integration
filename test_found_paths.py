"""
Test the found API paths with different parameters
"""

import requests
import json
from config import TIKAL_CONFIG

def test_paths():
    """Tests found paths with different parameters"""
    base_url = TIKAL_CONFIG['base_url'].rstrip('/')
    access_token = TIKAL_CONFIG.get('access_token', '')
    
    print("=" * 70)
    print("Testing Found API Paths")
    print("=" * 70)
    
    headers_json = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    headers_form = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    
    # Found paths that return 200
    paths_to_test = [
        '/cc3/index.php?format=json&action=agents',
        '/cc3/index.php?format=json&cat=agents',
        '/cc3/index.php?api=1&action=agents',
        '/cc3/index.php?output=json&action=agents',
    ]
    
    print("\nTesting paths with different methods and parameters...\n")
    
    for path in paths_to_test:
        url = f"{base_url}{path}"
        print(f"Testing: {path}")
        print("-" * 70)
        
        # Test 1: GET with JSON headers
        try:
            response = requests.get(url, headers=headers_json, timeout=5, verify=False)
            print(f"GET (JSON headers): {response.status_code}")
            content_type = response.headers.get('Content-Type', '')
            print(f"  Content-Type: {content_type}")
            
            # Try to parse as JSON
            try:
                data = response.json()
                print(f"  ✓ JSON response!")
                print(f"  Keys: {list(data.keys())[:10]}")
                print(f"  Sample: {json.dumps(data, indent=2, ensure_ascii=False)[:300]}")
                print("\n✓ SUCCESS! This is a working API endpoint!")
                print(f"Use this path: {path}\n")
                return path, data
            except:
                text_preview = response.text[:200]
                if 'json' in content_type.lower():
                    print(f"  JSON Content-Type but not parseable")
                    print(f"  Preview: {text_preview}")
                else:
                    print(f"  HTML response (preview): {text_preview[:100]}")
        except Exception as e:
            print(f"  Error: {e}")
        
        # Test 2: POST with JSON
        try:
            response = requests.post(
                url,
                json={'action': 'get_agents'},
                headers=headers_json,
                timeout=5,
                verify=False
            )
            if response.status_code not in [404, 405]:
                print(f"POST (JSON body): {response.status_code}")
                try:
                    data = response.json()
                    print(f"  ✓ JSON response!")
                    print(f"  Keys: {list(data.keys())[:10]}")
                    return path, data
                except:
                    pass
        except:
            pass
        
        # Test 3: GET with additional parameters
        try:
            # Add more parameters
            test_params = [
                {'format': 'json', 'action': 'agents', 'api': '1'},
                {'format': 'json', 'action': 'agents', 'output': 'json'},
                {'api': '1', 'action': 'agents', 'format': 'json', 'token': access_token},
            ]
            
            base_url_path = url.split('?')[0]
            for params in test_params:
                test_url = f"{base_url_path}?{requests.compat.urlencode(params)}"
                response = requests.get(test_url, headers=headers_json, timeout=5, verify=False)
                try:
                    data = response.json()
                    print(f"  ✓ JSON with params {params}!")
                    print(f"  Keys: {list(data.keys())[:10]}")
                    return test_url, data
                except:
                    pass
        except:
            pass
        
        print()
    
    print("=" * 70)
    print("No JSON API found in tested paths")
    print("=" * 70)
    print("\nThe paths return HTML, not JSON.")
    print("Possible reasons:")
    print("1. API needs to be enabled in settings")
    print("2. Different authentication method required")
    print("3. API uses different format (XML, SOAP)")
    print("4. Need to check PDF documentation for correct endpoints")


if __name__ == '__main__':
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    test_paths()

