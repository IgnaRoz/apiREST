import unittest
from tokensrv import command_handlers as ch
from flask import Flask, request, Response
import threading
import time

class TestApi(unittest.TestCase):

    def test_status(self):
        with ch.make_server("http://127.0.0.1:3001/api/v1").test_client()  as client:
            service = client.application.config['service_token']
            response = client.get('/api/v1/status')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode(), service.status_token())
    
    def test_make_token(self):
        server_auth = TestServerAuth()
        def run_server_test():
            server_auth.setUp().run(host='0.0.0.0', port=3005)

        # Create a new thread and start it
        server_thread = threading.Thread(target=run_server_test)
        server_thread.daemon = True  # Set the thread as a daemon thread
        server_thread.start()
        time.sleep(2)
        with ch.make_server("http://127.0.0.1:3005/api/v1").test_client() as client:
            service = client.application.config['service_token']
            response = client.put('/api/v1/token', json={'username': 'nacho', 'pass_hash': 'nacho_pass', 'expiration_cb': 'http://127.0.0.1:3005/api/v1/test'})
            token =response.json["token"]
            #print(service.tokens)
            #Confirmo que se ha creado el token
            self.assertIn(token, service.tokens)
            #Espero a que caduque el token
            time.sleep(4)
            #Compruebo que el token ha sido eliminado
            self.assertNotIn(token, service.tokens)
            #Compruebo que se ha lanzado el callback
            self.assertTrue(server_auth.flag)
            self.assertEqual(response.status_code, 200)


class TestServerAuth():

    def setUp(self):
        self.app = Flask(__name__)
        self.flag = False
        print('Setting up server')
        @self.app.route('/api/v1/test', methods=['PUT',])
        def test_route():
            self.flag = True
            #print('Received AUTH')
            return Response('Received AUTH', 200)
        @self.app.route('/api/v1/alive', methods=['GET',])
        def alive():
            print('ESTOY VIVO')
            return Response('Servicio de auth activo', 200)
        #self.app.test_client(host='0.0.0.0', port=3005)
        @self.app.route('/api/v1/is_authorized/<token>', methods=['GET',])
        def is_authorized(token):
            #print('ES AUTORIZADO')
            return  Response('ES AUTORIZADO', 200) 
        

        return self.app

  