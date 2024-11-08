import requests
ROOT_API = 'http://127.0.0.1:3002/api/v1'    


#crear token
response = requests.put(ROOT_API + '/token', json={"username":"user","pass_hash":"pass"})

print(response.status_code)
print(response.json())