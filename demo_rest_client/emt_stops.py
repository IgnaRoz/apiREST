#!/usr/bin/env python3

import copy

import requests


BASE_HEADERS = {
    'content-type': 'application/json',
    'accepts': 'application/json'
}


class EMTApi:
    def __init__(self, apiRoot, email, password):
        self._uri_ = f'{apiRoot}v1/' if apiRoot.endswith('/') else f'{apiRoot}/v1/'
        self._email_ = email
        self._passw_ = password

    @property
    def accessToken(self):
        return '8389aadb-7cae-4b5d-8bcc-b3fbc8b77ae7'

    @property
    def authenticated_headers(self):
        h = copy.copy(BASE_HEADERS)
        h.update({'accessToken': self.accessToken})
        return h

    def getStops(self, stops):
        uri = f'{self._uri_}transport/busemtmad/stops/list/'
        req = requests.post(
            uri,
            headers=self.authenticated_headers,
            json=stops
        )
        if req.status_code != 200:
            raise RuntimeError(f'Unexpected response code from server ({req.status_code})')

        result = []
        for stop in req.json()['data']:
            result.append(BusStop(**stop))
        return result

    def updateStop(self, stop):
        uri = f'https://openapi.emtmadrid.es/v1/transport/busemtmad/stops/{stop.node}/'
        req = requests.post(uri, headers=self.client_headers, json=stop.as_dict)


class BusStop:
    '''Representacion de una parada de bus'''
    def __init__(self, **kwargs):
        self.node = kwargs.pop('node')
        self.geometry = kwargs.pop('geometry', None)
        self.name = kwargs.pop('name')
        self.wifi = kwargs.pop('wifi')
        self.lines = kwargs.pop('lines', [])

    @property
    def as_dict(self):
        return {
            'node': self.node,
            'geometry': self.geometry,
            'name': self.name,
            'wifi': self.wifi,
            'lines': self.lines
        }

    def __str__(self):
        return f'Stop({self.node}): {self.name} [{self.lines}]'


api = EMTApi('https://openapi.emtmadrid.es', '', '')
for stop in api.getStops([1, 2, 3, 4, 5, 6]):
    print(stop)

