import logging

from modules import gui
from modules import server_requests


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.DEBUG)

client = gui.Client()

client.window.mainloop()