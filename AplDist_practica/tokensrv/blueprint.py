from flask import Blueprint, Response,current_app

token_api = Blueprint('token_api', __name__)

ROOT_API = '/api/v1'

@token_api.route(f'{ROOT_API}/status', methods=('GET',))
def status():
    servicio_token = current_app.config['service_token']

    print (servicio_token.status_token())
    return Response(servicio_token.status_token(), status=200)