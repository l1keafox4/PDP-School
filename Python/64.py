text = {}

import json
text_json = json.dumps(text)

import requests
url = 'https://example.com/'
response = requests.post(url, data=text_json)
print (response.status_code)