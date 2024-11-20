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
    def test_make_token(self):
        """Test the make_token endpoint."""
        #crear token
        response = requests.put(URI_TOKEN+"/token",
                            json={"username":ADMIN_USERNAME,
                            "pass_hash":ADMIN_PASS_HASH})
        self.assertEqual(response.status_code, 200)
        token =response.json()["token"]
        #comprobar que se ha creado el token
        response = requests.get(URI_TOKEN+f"/token/{token}")
        self.assertEqual(response.status_code, 200)
        #comprobar que el username de la respuesta
        self.assertEqual(response.json()["username"], ADMIN_USERNAME)
        #comprobar que dentro del array roles se encuentra el rol admin
        self.assertIn("admin", response.json()["roles"])
    
    def test_delete_token(self):
        """Test the delete_token endpoint."""
        #crear token
        response = requests.put(URI_TOKEN+"/token",
                            json={"username":ADMIN_USERNAME,
                            "pass_hash":ADMIN_PASS_HASH})
        self.assertIn(response.status_code, [200, 204])
        token =response.json()["token"]
        #borrar token
        response = requests.delete(URI_TOKEN+f"/token/{token}", headers={"Owner":ADMIN_USERNAME})
        self.assertEqual(response.status_code, 204)
        




