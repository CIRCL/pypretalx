#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from urllib.parse import urljoin


class PyPretalxError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self)


class PyPretalxMissingAuthParameter(PyPretalxError):
    pass


class PyPretalxUnexpectedResponse(PyPretalxError):
    pass


class PyPretalx():

    def __init__(self, url: str, username: str=None, password: str=None, token: str=None):
        self.root_url = url
        if username and password:
            self._get_token(username, password)
        elif token:
            self.token = token
        else:
            raise PyPretalxMissingAuthParameter('You need to pass (username AND password) OR token.')
        self.headers = {
            'user-agent': 'PyPretalx',
            'Authorization': f'Token {self.token}',
            'Accept': 'application/json'
        }

    def _get_token(self, username: str, password: str):
        url = urljoin(self.root_url, '/api/auth/')
        data = {'username': username, 'password': password}
        r = requests.post(url, data=data)
        j = r.json()
        if 'token' not in j:
            raise PyPretalxUnexpectedResponse(r.text)
        self.token = j['token']

    def _generic_get(self, event: str=None, endpoint: str=None, code: str=None, **params):
        base_path = '/api/events/'
        if event:
            base_path = f'{base_path}{event}/'
        if endpoint:
            base_path = f'{base_path}{endpoint}/'
        if code:
            base_path = f'{base_path}{code}'
        url = urljoin(self.root_url, base_path)
        r = requests.get(url, params=params, headers=self.headers)
        return r.json()

    def me(self):
        url = urljoin(self.root_url, '/api/me')
        r = requests.get(url, headers=self.headers)
        return r.json()

    def events(self, event: str=None, **params):
        return self._generic_get(event, **params)

    def submissions(self, event: str, code: str=None, **params):
        return self._generic_get(event, 'submissions', code, **params)

    def talks(self, event: str, code: str=None, **params):
        return self._generic_get(event, 'talks', code, **params)

    def speakers(self, event: str, code: str=None, **params):
        return self._generic_get(event, 'speakers', code, **params)

    def reviews(self, event: str, code: str=None, **params):
        return self._generic_get(event, 'reviews', code, **params)

    def rooms(self, event: str, code: str=None, **params):
        return self._generic_get(event, 'rooms', code, **params)
