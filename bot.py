import requests

api_key = 'Sk_live_1x7jN6OUqTIzUNEv7MIM9Er2h5GphCXer9ef4BUx'
url = 'https://redxsms.com/api/v1/iprn'

headers = {
    'Authorization': f'Bearer {api_key}',
    'Accept': 'application/json'
}

response = requests.get(url, headers=headers)
print("Status Code:", response.status_code)
print("Full Response Text:", response.text)
