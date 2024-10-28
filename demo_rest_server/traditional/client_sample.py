#!/usr/bin/env python3

from typing import List

import requests


def _assert_status_ok_(status_code):
    if status_code not in [200, 204]:
        raise RuntimeError('Unknown response from API')


class RestList:
    def __init__(self, root_api: str) -> None:
        self._root_api_ = root_api
        if not self.status_ok:
            raise ValueError(f'Invalid API root "{root_api}"')

    @property
    def status_ok(self):
        request = requests.get(f'{self._root_api_}/status')
        _assert_status_ok_(request.status_code)
        return True

    @property
    def items(self) -> List[str]:
        request = requests.get(f'{self._root_api_}/items')
        _assert_status_ok_(request.status_code)
        return str(request.content.decode('UTF-8')).splitlines()

    def add(self, item: str) -> None:
        if not isinstance(item, str):
            raise ValueError(item)
        response = requests.put(f'{self._root_api_}/item', json={
            'item': item
        })
        _assert_status_ok_(response.status_code)

    def remove(self, item: str) -> None:
        if not isinstance(item, str):
            raise ValueError(item)
        response = requests.delete(f'{self._root_api_}/item/{item}')
        if response.status_code == 404:
            raise ValueError("list.remove(x): x not in list")
        _assert_status_ok_(response.status_code)


class RemoteStoredList(list):
    def __init__(self, remote_list: RestList) -> None:

        self._rlist_ = remote_list

    def clear(self):
        for i in self._rlist_.items:
            self._rlist_.remove(i)


if __name__ == '__main__':
    cli = RestList('http://localhost:5000/api/v1')
    cli.add('hola')
    cli.add('adios')
    cli.remove('hola')
    print(cli.items)
    cli.remove('hola')
