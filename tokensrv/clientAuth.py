#!/usr/bin/env python3

"""ClientAuth module."""

import hashlib
import requests

class ClientAuth:
    def __init__(self, URI: str):
        self.URI = URI
        

    def status(self):
        try:
            response = requests.get(f'{self.URI}/alive', timeout=5)
        except requests.exceptions.RequestException as e:
            return False
        
        return response.status_code in (200, 201,204)
    
    
    def is_authorized(self, user:str,pass_hash:str):
        #Calcular el authToken: hash(username + password)
        try:

            auth_string = user + pass_hash

            # Calculate the authToken using SHA-256
            auth_token = hashlib.sha256(f'{user}{pass_hash}'.encode()).hexdigest()
            response = requests.get(f'{self.URI}/is_authorized/{auth_token}')
            return response.status_code in (200, 201,204)
        except requests.exceptions.RequestException as e:
            return False