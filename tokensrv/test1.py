
#import service_token as Service_token 
from flask import Flask, request, jsonify

from service_token import  Service_token
import blueprint



def test_make_token():
    app = Flask(__name__, instance_relative_config=True)
    app.config['service_token'] = Service_token()
    app.register_blueprint(blueprint.token_api)
    with app.test_client() as client:
        response =  client.put('/api/v1/token', json={"username":"user","pass_hash":"pass"})

if __name__ == '__main__':
    test_make_token()