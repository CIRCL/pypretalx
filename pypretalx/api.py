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

    def me(self):
        url = urljoin(self.root_url, '/api/me')
        r = requests.get(url, headers=self.headers)
        return r.json()

    def talks(self, event: str, code: str=None, **params):
        if code:
            url = urljoin(self.root_url, f'/api/events/{event}/talks/{code}')
        else:
            url = urljoin(self.root_url, f'/api/events/{event}/talks/')
        r = requests.get(url, params=params, headers=self.headers)
        return r.json()

    def speakers(self, event: str, code: str=None, **params):
        if code:
            url = urljoin(self.root_url, f'/api/events/{event}/speakers/{code}')
        else:
            url = urljoin(self.root_url, f'/api/events/{event}/speakers/')
        r = requests.get(url, params=params, headers=self.headers)
        return r.json()
