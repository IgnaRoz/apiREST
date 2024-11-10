"""Blueprint for the token service."""

import json
from flask import Blueprint, request, Response,current_app
from tokensrv.service_token import Forbidden, TokenNotFound

token_api = Blueprint('token_api', __name__)

ROOT_API = '/api/v1'

@token_api.route(f'{ROOT_API}/status', methods=('GET',))
def status():
    """Return the status of the service."""
    servicio_token = current_app.config['service_token']
    logger = current_app.config['logger']
    logger.info('Status token')
    #print (servicio_token.status_token())
    return Response(servicio_token.status_token(), status=200)

@token_api.route(f'{ROOT_API}/token', methods=('PUT',))
def make_token():
    """Create a new token."""
    #Registrar ip de origen y enviar 400 despues de x intentos?
    if "username" not in request.json or "pass_hash" not in request.json:
        return Response('JSON data expected', status=400)

    username = request.json['username']
    password = request.json['pass_hash']

    servicio_auth = current_app.config['service_auth']
    if not servicio_auth.is_authorized(username,password):
        return Response('Unauthorized', status=401)
    if "expiration_cb" not in request.json:
        expiration_cb = None
    else:
        expiration_cb = request.json['expiration_cb']

    servicio_token = current_app.config['service_token']
    token,live_time = servicio_token.make_token(username,expiration_cb)
    #Make token no lanza la excepcion Forbidden


    return Response(json.dumps({"token":token,"live_time":live_time}),
                     status=200, mimetype='application/json')


@token_api.route(f'{ROOT_API}/token/<token>', methods=('DELETE',))
def delete_token(token):
    """Delete a token."""
    if "Owner" not in request.headers.keys():
        return Response('Ownerheader expected', status=400)

    servicio_token = current_app.config['service_token']
    try:
        servicio_token.delete_token(token)
    except Forbidden as e: #Exception Forbidden
        return Response(str(e), status=401)
    except TokenNotFound as e: #Ecxeption TokenNotFound
        return Response(str(e), status=404)

    return Response('Token deleted', status=204)



@token_api.route(f'{ROOT_API}/token/<token>', methods=('GET',))
def get_token(token):
    """Return the token info."""
    servicio_token = current_app.config['service_token']
    try:
        username,roles = servicio_token.get_token(token)
    except TokenNotFound as e: #Exception TokenNotFound
        return Response(str(e), status=404)

    return Response(json.dumps({"username":username,"roles":roles})
                    , status=200)
