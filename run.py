import logging

from modules import gui
from modules import server_requests


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.DEBUG)

server_url = input('Input server URL: ')

conn = server_requests.Clipboard_conn(server_url)

gui.render_gui(conn)