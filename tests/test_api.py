import unittest
from tokensrv import command_handlers as ch
from flask import Flask, request, Response
import threading
import time
import requests
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
    
    



#clase de para lanzar un servidor de auth para los test
#Implementa un singleton para que solo se lance un servidor de auth para todo(ya que una vez lanzado no se puede parar)
class TestServerAuth:
    __test__ = False #Para que pytest lo ignore
    _instance = None

    @staticmethod
    def getInstance():
        if TestServerAuth._instance is None:
            TestServerAuth._instance = TestServerAuth()
        return TestServerAuth._instance

    def __init__(self):
        if TestServerAuth._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            TestServerAuth._instance = self
            
        self.app = Flask(__name__)
        self.flag = False
        print('Setting up server')
        @self.app.route('/api/v1/test', methods=['PUT',])
        def test_route():
            TestServerAuth.getInstance().flag = True
            return Response('Received AUTH', 200)
        @self.app.route('/api/v1/alive', methods=['GET',])
        def alive():
            return Response('Servicio de auth activo', 200)
        #self.app.test_client(host='0.0.0.0', port=3005)
        @self.app.route('/api/v1/is_authorized/<token>', methods=['GET',])
        def is_authorized(token):
            return  Response('ES AUTORIZADO', 200) 
        
        def run_server_test():
            self.app.run(host='0.0.0.0', port=3005)

        # Create a new thread and start it
        server_thread = threading.Thread(target=run_server_test)
        server_thread.daemon = True  # Set the thread as a daemon thread
        server_thread.start()

  