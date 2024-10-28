#!/usr/bin/env python3

from flask import Blueprint, Response, current_app, request

api = Blueprint('rlist_api', __name__)

ROOT_API = '/api/v1'

@api.route(f'{ROOT_API}/status', methods=('GET',))
def status():
    return Response('', status=204)

@api.route(f'{ROOT_API}/items', methods=('GET',))
def items():
    service = current_app.config['service']
    return Response('\n'.join(service.items), status=200)

@api.route(f'{ROOT_API}/item', methods=('PUT',))
def add_item():
    service = current_app.config['service']
    if not request.json:
        return Response('JSON data expected', status=400)
    try:
        item = request.json['item']
    except KeyError as error:
        return Response(f'Missing key: {error}', status=400)
    try:
        service.add(item)
    except ValueError:
        return Response(f'Bad request', status=400)
    return Response('', status=204)

@api.route(f'{ROOT_API}/item/<item>', methods=('DELETE',))
def remove_item(item):
    service = current_app.config['service']
    try:
        service.remove(item)
    except ValueError:
        return Response('', status=404)
    return Response('', status=204)
