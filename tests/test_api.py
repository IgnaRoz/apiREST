"""Tests for the API of the token server."""

import hashlib
import socket
from time import sleep
import unittest
import requests
from tokensrv import command_handlers as ch
import pytest

ADMIN_USERNAME = 'administrator'
ADMIN_PASS_HASH = hashlib.sha256('adminpass'.encode()).hexdigest()
ADMIN_AUTH_CODE = hashlib.sha256(f'{ADMIN_USERNAME}{ADMIN_PASS_HASH}'.encode()).hexdigest()
USER_USERNAME = 'user'
USER_PASS_HASH = hashlib.sha256('userpass'.encode()).hexdigest()
USER_PASS_CODE = hashlib.sha256(f'{USER_USERNAME}{USER_PASS_HASH}'.encode()).hexdigest()
URI_AUTH = 'http://127.0.0.1:3000/auth/v1'
#URI_AUTH = 'http://127.0.0.1:3001/api/v1'


class TestApi(unittest.TestCase):
    """Tests for the API of the token server."""


    @pytest.fixture(scope="session", autouse=True)
    def setup_once(self):
        # Coloca aquí el código que quieres ejecutar al inicio
        print("Ejecutando setup al inicio de los tests")
        with ch.make_server(URI_AUTH).test_client()  as client:


            headers = {"Content-Type": "application/json","AuthToken":"token_for_admin"}
            response = client.patch('/auth/v1/user', json={'username':USER_USERNAME, 'password':USER_PASS_HASH,'role':'admin'}, headers=headers)
            assert response.status_code == 200

    def test_alive_mock(self):
        """Test the alive endpoint."""
        response = requests.get(URI_AUTH+"/status",timeout=5)
        #print(response.text)
        self.assertEqual(response.status_code, 204)

    def test_status(self):
        """Test the status endpoint."""
        with ch.make_server(URI_AUTH).test_client()  as client:
            service = client.application.config['service_token']
            response = client.get('/api/v1/status')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode(), service.status_token())

    def test_make_token(self):
        """Test the make_token endpoint."""
        server =ch.make_server(URI_AUTH)
        with server.test_client()  as client:

            service = client.application.config['service_token']
            response = client.put('/api/v1/token',
                            json={"username":USER_USERNAME,
                            "pass_hash":USER_PASS_HASH,
                            "expiration_cb":"http://127.0.0.1:3018/api/v1/alive"})
            self.assertEqual(response.status_code, 200)
            token =response.json["token"]
            #Confirmo que se ha creado el token
            self.assertIn(token, service.tokens.keys())
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.bind(("127.0.0.1", 3018))
                server_socket.listen()
                # Aceptar una conexión entrante
                client_socket,_  = server_socket.accept()
                #print(f"Conexión desde {client_address}")
                # Recibir datos del cliente
                client_socket.recv(2048)
                #print(f"Recibido: {data.decode()}")
                # Enviar datos al cliente

                client_socket.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
                # Cerrar la conexión
                client_socket.close()

            #sleep(9)#Espera a que caduquen los tokens
            #Compruebo que el token ha sido eliminado
            self.assertNotIn(token, service.tokens.keys())
    def test_make_token_BadRequest(self):
        server =ch.make_server(URI_AUTH)
        with server.test_client()  as client:
            response = client.put('/api/v1/token',
                            json={"name":USER_USERNAME,
                            "pass":USER_PASS_HASH})
            self.assertEqual(response.status_code, 400)
    def test_make_token_Unauthorized(self):
        server =ch.make_server(URI_AUTH)
        with server.test_client()  as client:
            response = client.put('/api/v1/token',
                            json={"username":USER_USERNAME,
                            "pass_hash":"bad_hash"})
            self.assertEqual(response.status_code, 401)
    def test_delete_token(self):
        server =ch.make_server(URI_AUTH)
        with server.test_client()  as client:
            service = client.application.config['service_token']
            token,_ = service.make_token(USER_USERNAME)
            response = client.delete(f'/api/v1/token/{token}',headers={"Owner":USER_USERNAME})
            #Compruebo que el token ha sido eliminado
            self.assertNotIn(token, service.tokens.keys())
            #Compruebo el codigo de respuesta
            self.assertEqual(response.status_code, 204)
    def test_delete_token_not_owner(self):
        server =ch.make_server(URI_AUTH)
        with server.test_client()  as client:
            service = client.application.config['service_token']
            token,_ = service.make_token(USER_USERNAME)
            response = client.delete(f'/api/v1/token/{token}')
            #Compruebo que el token NO ha sido eliminado
            self.assertIn(token, service.tokens.keys())
            #Compruebo el codigo de respuesta
            self.assertEqual(response.status_code, 400)
    def test_delete_token_Forbidden(self):
        server =ch.make_server(URI_AUTH)
        with server.test_client()  as client:
            service = client.application.config['service_token']
            token,_ = service.make_token(USER_USERNAME)
            response = client.delete(f'/api/v1/token/{token}',headers={"Owner":"NotOwner"})
            #Compruebo que el token NO ha sido eliminado
            self.assertIn(token, service.tokens.keys())
            #Compruebo el codigo de respuesta
            self.assertEqual(response.status_code, 401)
    def test_delete_token_not_found(self):

        server =ch.make_server(URI_AUTH)

        with server.test_client()  as client:
            service = client.application.config['service_token']
            token,_ = service.make_token(USER_USERNAME)
            response = client.delete(f'/api/v1/token/NotToken',headers={"Owner":USER_USERNAME})
            #Compruebo que el token NO ha sido eliminado
            self.assertIn(token, service.tokens.keys())
            #Compruebo el codigo de respuesta
            self.assertEqual(response.status_code, 404)
    def test_get_token(self):
        """Test the get_token endpoint."""
        server =ch.make_server(URI_AUTH)
        with server.test_client()  as client:
            #crea un token sin expiration_cb
            service = client.application.config['service_token']
            response = client.put('/api/v1/token',
                            json={"username":USER_USERNAME,"pass_hash":USER_PASS_HASH})
            self.assertEqual(response.status_code, 200)
            #Se comprueba que el token se ha creado
            token =response.json["token"]
            self.assertIn(token, service.tokens.keys())
            #Se accede a api/v1/token/<token> para obtener el dueño y los roles
            response = client.get(f'/api/v1/token/{token}')
            self.assertEqual(response.status_code, 200)
            #Se comprueba que la informacion del token es correcta
            self.assertEqual(response.json["username"], USER_USERNAME)
            #Se comprueba que se obtiene un array de roles
            #print(response.json)
            self.assertIsInstance(response.json["roles"], list)
            #se comprueba que los roles de USER_USERNAME son ["user"]
            self.assertEqual(response.json["roles"], ["user"])
            #Espera a que caduque el token
            #sleep(6)
    def test_get_token_not_found(self):
        """Test the get_token endpoint."""
        server =ch.make_server(URI_AUTH)
        with server.test_client()  as client:
            #crea un token sin expiration_cb
            service = client.application.config['service_token']
            response = client.put('/api/v1/token',
                            json={"username":USER_USERNAME,"pass_hash":USER_PASS_HASH})
            self.assertEqual(response.status_code, 200)
            #Se comprueba que el token se ha creado
            token =response.json["token"]
            self.assertIn(token, service.tokens.keys())
            #Se accede a api/v1/token/<token> para obtener el dueño y los roles
            response = client.get(f'/api/v1/token/NotToken')
            self.assertEqual(response.status_code, 404)