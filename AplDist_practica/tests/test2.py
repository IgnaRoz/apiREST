import requests
import time
import random
import asyncio

ROOT_API = 'http://127.0.0.1:3002/api/v1'    


def enviar_token():
#crear token
    requests.put(ROOT_API + '/token', json={"username":"user","pass_hash":"pass"},hooks={'response':[print_response]})
    print('Token enviado')



def print_response(response, *args, **kwargs):
    print(response.status_code)
    print(response.json())



async def main(loop, iterations):
    futures = []

    for i in range(iterations):
        future = loop.run_in_executor(None, enviar_token)
        futures.append(future)

    for future in futures:
        r = await future  
    

def run(iterations):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop,iterations))

if __name__ == '__main__':
    run(20)