
from flask import Blueprint, current_app, request, Response


sample_api = Blueprint('sample_api', __name__)

ROOT_API = '/api/v1'


@sample_api.route(f'{ROOT_API}/hello', methods=('GET',))
def hello():
    return Response('Service running', status=200)
