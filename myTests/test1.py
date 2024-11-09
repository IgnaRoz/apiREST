import requests
ROOT_API = 'http://127.0.0.1:3002/api/v1'    


#crear token
response = requests.get(ROOT_API + '/status')

print(response.status_code)
print(response.text)