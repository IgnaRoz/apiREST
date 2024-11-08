import requests
import hashlib
import time
import random
import asyncio

ROOT_API = 'http://127.0.0.1:3002/api/v1'    
CALL_BACK = 'http://127.0.0.1:3002/api/v1/status'   

ADMIN_USERNAME = 'administrator'
ADMIN_PASS_HASH = hashlib.sha256('adminpass'.encode()).hexdigest()
ADMIN_AUTH_CODE = hashlib.sha256(f'{ADMIN_USERNAME}{ADMIN_PASS_HASH}'.encode()).hexdigest()
USER_USERNAME = 'user'
USER_PASS_HASH = hashlib.sha256('userpass'.encode()).hexdigest()
USER_PASS_CODE = hashlib.sha256(f'{USER_USERNAME}{USER_PASS_HASH}'.encode()).hexdigest()



def enviar_token():
#crear token con usuario del mock
    response = requests.put(ROOT_API + '/token', json={"username":USER_USERNAME,"pass_hash":USER_PASS_HASH, "expiration_cb": CALL_BACK },hooks={'response':[print_response]})


    print('Token enviado')



def print_response(response, *args, **kwargs):
    print(response.status_code)
    print(response.json())


if __name__ == '__main__':
    enviar_token()