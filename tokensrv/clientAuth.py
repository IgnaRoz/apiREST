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
            response = requests.get(f'{self.uri}/auth/{auth_token}', timeout=5)
            return response.status_code in (200, 201,204)
        except requests.exceptions.RequestException:
            return False
    def get_roles(self, user:str, token:str):
        """Get the roles of the user."""
        try:
            response = requests.get(f'{self.uri}/user/{user}',
                                    headers={"AuthToken":token},
                                      timeout=5)
            return response.json()['roles']
        except requests.exceptions.RequestException:
            return False
