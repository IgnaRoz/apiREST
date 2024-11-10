#!/usr/bin/env python3

"""ClientAuth module."""

import hashlib
import requests

class ClientAuth:
    """ClientAuth class."""
    def __init__(self, uri: str):
        self.uri = uri

    def status(self):
        """Check if the service is alive."""
        try:
            response = requests.get(f'{self.uri}/alive', timeout=5)
        except requests.exceptions.RequestException:
            return False

        return response.status_code in (200, 201,204)


    def is_authorized(self, user:str,pass_hash:str):
        """Check if the user is authorized."""

        try:

            # ElauthToken: hash(username + password)
            # Calculate the authToken using SHA-256
            auth_token = hashlib.sha256(f'{user}{pass_hash}'.encode()).hexdigest()
            response = requests.get(f'{self.uri}/is_authorized/{auth_token}',timeout=10)
            return response.status_code in (200, 201,204)
        except requests.exceptions.RequestException:
            return False
