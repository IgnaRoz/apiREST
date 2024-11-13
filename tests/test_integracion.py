import hashlib
import unittest
import requests

ADMIN_USERNAME = 'administrator'
ADMIN_PASS_HASH = hashlib.sha256('admin2024'.encode()).hexdigest()
ADMIN_AUTH_CODE = hashlib.sha256(f'{ADMIN_USERNAME}{ADMIN_PASS_HASH}'.encode()).hexdigest()
USER_USERNAME = 'user'
USER_PASS_HASH = hashlib.sha256('userpass'.encode()).hexdigest()
USER_PASS_CODE = hashlib.sha256(f'{USER_USERNAME}{USER_PASS_HASH}'.encode()).hexdigest()
URI_AUTH = 'http://127.0.0.1:3000/auth/v1'
#URI_AUTH = 'http://127.0.0.1:3001/api/v1'
URI_TOKEN = 'http://127.0.0.1:3002/api/v1'

class TestIntegracion(unittest.TestCase):
    

    def test_services_alive(self):
        """Test the status endpoint."""
        #comprobar estado del servicio de autenticación sea 200 o 204
        response = requests.get(URI_AUTH+"/status",timeout=5)
        self.assertIn(response.status_code, [200, 204])

        #comprobar estado del servicio de tokens
        response = requests.get(URI_TOKEN+"/status",timeout=5)
        self.assertIn(response.status_code, [200, 204])