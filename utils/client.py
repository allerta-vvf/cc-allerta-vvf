import requests
from cat.plugins.allerta_vvf.settings import get_setting

def api_request(cat, url, method="GET", payload=None):
    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer "+get_setting(cat, "login_token")
    }
    
    url = get_setting(cat, "api_url")+url
    response = requests.request(method, url, json=payload, headers=headers)
    response.raise_for_status()
    
    if response.headers['content-type'] == 'application/json':
        return response.json()
    else:
        return response.text
