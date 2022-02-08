import requests
import logging

class Clipboard_conn:
    def __init__(self, server_url):
        self.resource_url = server_url + '/api/clipboard'

    def get_clipboard(self):
        r = requests.get(self.resource_url)

        logging.debug('GET Request against {} with status code {}'.format(self.resource_url, r.status_code))
        assert r.status_code == 200

        return r.content

    def post_clipboard(self, text):
        r = requests.post(self.resource_url, json={'text': text})

        logging.debug('POST Request against {} with status code {}'.format(self.resource_url, r.status_code))
        assert r.status_code == 201

        return r.content

    def delete_clipboard(self):
        r = requests.delete(self.resource_url)

        logging.debug('DELETE Request against {} with status code {}'.format(self.resource_url, r.status_code))
        assert r.status_code == 200

        return r.content