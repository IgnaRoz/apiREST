import unittest
from tokensrv import command_handlers as ch

class TestApi(unittest.TestCase):

    def test_status(self):
        with ch.make_server("0.0.0.0", 3002, "http://127.0.0.1:3001/api/v1").test_client()  as client:
            service = client.application.config['service_token']
            response = client.get('/api/v1/status')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode(), service.status_token())