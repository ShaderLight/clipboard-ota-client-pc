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

    def connection_test(self):
        try:
            r = self.post_clipboard('test')
            assert r['text'] == 'test'

            r = self.get_clipboard()
            assert r['text'] == 'test'

            r = self.delete_clipboard()
            assert r['text'] == ''

        except:
            return False

        return True

    def change_url(self, new_url):
        old_url = self.resource_url
        self.resource_url = new_url + '/api/clipboard'

        if self.connection_test():
            logging.debug('Connection test succeded, url changed.')
        else:
            logging.debug('Connection test failed, reverting url.')
            self.resource_url = old_url


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