import requests
ROOT_API = 'http://127.0.0.1:3002/api/v1'    

import hashlib


ADMIN_USERNAME = 'administrator'
ADMIN_PASS_HASH = hashlib.sha256('adminpass'.encode()).hexdigest()
ADMIN_AUTH_CODE = hashlib.sha256(f'{ADMIN_USERNAME}{ADMIN_PASS_HASH}'.encode()).hexdigest()
USER_USERNAME = 'user'
USER_PASS_HASH = hashlib.sha256('userpass'.encode()).hexdigest()
USER_PASS_CODE = hashlib.sha256(f'{USER_USERNAME}{USER_PASS_HASH}'.encode()).hexdigest()

#crear token
response = requests.put(ROOT_API + '/token', json={"username":USER_USERNAME,"pass_hash":USER_PASS_HASH})

print(response.status_code)
print(response.json())