from time import sleep
import unittest
from tokensrv import command_handlers as ch
from flask import Flask, request, Response
import hashlib
import requests
import socket
import json

ADMIN_USERNAME = 'administrator'
ADMIN_PASS_HASH = hashlib.sha256('adminpass'.encode()).hexdigest()
ADMIN_AUTH_CODE = hashlib.sha256(f'{ADMIN_USERNAME}{ADMIN_PASS_HASH}'.encode()).hexdigest()
USER_USERNAME = 'user'
USER_PASS_HASH = hashlib.sha256('userpass'.encode()).hexdigest()
USER_PASS_CODE = hashlib.sha256(f'{USER_USERNAME}{USER_PASS_HASH}'.encode()).hexdigest()




class TestApi(unittest.TestCase):
    def test_alive_Mock(self):
        response = requests.get("http://127.0.0.1:3001/api/v1/alive")
        print(response.text)
        self.assertEqual(response.status_code, 204)

    def test_status(self):
        with ch.make_server("http://127.0.0.1:3001/api/v1").test_client()  as client:
            service = client.application.config['service_token']
            response = client.get('/api/v1/status')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode(), service.status_token())
    
    def test_make_token(self):
        server =ch.make_server("http://127.0.0.1:3001/api/v1")
        with server.test_client()  as client:
            
            service = client.application.config['service_token']
            response = client.put('/api/v1/token', json={"username":USER_USERNAME,"pass_hash":USER_PASS_HASH,"expiration_cb":"http://127.0.0.1:3018/api/v1/alive"})
            self.assertEqual(response.status_code, 200)
            token =response.json["token"]
            #Confirmo que se ha creado el token
            self.assertIn(token, service.tokens.keys())
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.bind(("127.0.0.1", 3018))
                server_socket.listen()
                # Aceptar una conexión entrante
                client_socket, client_address = server_socket.accept()
                print(f"Conexión desde {client_address}")
                # Recibir datos del cliente
                data = client_socket.recv(2048)
                print(f"Recibido: {data.decode()}")
                # Enviar datos al cliente
                
                client_socket.send(b"HTTP/1.1 200 OK\r\n\r\n")
                # Cerrar la conexión
                client_socket.close()

            #sleep(9)#Espera a que caduquen los tokens
            #Compruebo que el token ha sido eliminado
            print(f'Los tokens son {service.tokens}')
            self.assertNotIn(token, service.tokens.keys())

            
            
            
    
    


