#!/usr/bin/env python3

"""ClientAuth module."""

import hashlib
import requests

class ClientAuth:
    """ClientAuth class."""

    def __init__(self, uri: str):
        """Initialize the class."""
        self.uri = uri


    def status(self):
        """Return the status of the service."""
        try:
            response = requests.get(f'{self.uri}/status', timeout=5)
        except requests.exceptions.RequestException:
            return False

        return response.status_code in (200, 201,204)

    def is_authorized(self, user:str,pass_hash:str):
        """Check if the user is authorized."""
        try:
            # Calculate the authToken using SHA-256. auth_string = user + pass_hash
            auth_token = hashlib.sha256(f'{user}{pass_hash}'.encode()).hexdigest()
            response = requests.get(f'{self.uri}/is_authorized/{auth_token}', timeout=5)
            if response.status_code not in (200, 201,204):
                return []
            return response.json()['roles']
        except requests.exceptions.RequestException:
            return []
