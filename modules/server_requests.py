from ast import match_case
from urllib import response
import requests
import logging
from threading import Thread


class Clipboard_conn:
    def __init__(self, server_url):
        self.resource_url = server_url + '/api/clipboard'

    def get_clipboard(self):
        r = requests.get(self.resource_url)

        logging.debug('GET Request against {} with status code {}'.format(self.resource_url, r.status_code))
        assert r.status_code == 200

        return r.json()

    def post_clipboard(self, text):
        r = requests.post(self.resource_url, json={'text': text})

        logging.debug('POST Request against {} with status code {}'.format(self.resource_url, r.status_code))
        assert r.status_code == 201

        return r.json()

    def delete_clipboard(self):
        r = requests.delete(self.resource_url)

        logging.debug('DELETE Request against {} with status code {}'.format(self.resource_url, r.status_code))
        assert r.status_code == 200

        return r.json()

    def is_connected(self):
        r = requests.get(self.resource_url)

        return r.status_code == 200


class ConnectionThread(Thread):
    def __init__(self, conn, method, text=None):
        super().__init__()
        self.conn = conn
        self.method = method
        self.text = text
        self.response = None

    def run(self):
        match self.method:
            case 'get':
                self.response = self.conn.get_clipboard()
            case 'post':
                self.response = self.conn.post_clipboard(self.text)
            case 'delete':
                self.response = self.conn.delete_clipboard()