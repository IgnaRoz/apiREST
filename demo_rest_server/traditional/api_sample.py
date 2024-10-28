#!/usr/bin/env python3

from flask import Flask, Response, request

app = Flask(__name__)

ROOT_API = '/api/v1'
STORAGE = list()


@app.route(f'{ROOT_API}/status', methods=('GET',))
def hello():
    return Response('', status=204)

@app.route(f'{ROOT_API}/item', methods=('PUT',))
def add_item():
    global STORAGE
    if not request.json:
        return Response('JSON data expected', status=400)
    try:
        item = request.json['item']
    except KeyError as error:
        return Response(f'Missing key: {error}', status=400)

    STORAGE.append(item)
    return Response('', status=204)

@app.route(f'{ROOT_API}/items', methods=('GET',))
def get_full_list():
    global STORAGE
    if not STORAGE:
        return Response('', status=204)
    result = '\n'.join(STORAGE)
    return Response(result, status=200)

@app.route(f'{ROOT_API}/item/<item>', methods=('DELETE',))
def remove_item(item):
    global STORAGE
    try:
        STORAGE.remove(item)
    except ValueError:
        return Response('', status=404)
    return Response('', status=204)


if __name__ == '__main__':
    app.run(debug=True)
