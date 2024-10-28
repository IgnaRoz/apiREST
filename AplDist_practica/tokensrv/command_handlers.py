from service_token import  Service_token
import blueprint
#import service_token as Service_token 
from flask import Flask, request, jsonify


def run_server():
    app = Flask(__name__, instance_relative_config=True)
    app.config['service_token'] = Service_token()
    app.register_blueprint(blueprint.token_api)
    app.run(debug=True)

if __name__ == '__main__':
    run_server()