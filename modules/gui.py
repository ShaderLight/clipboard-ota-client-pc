import tkinter as tk
import tkinter.ttk as ttk

from .server_requests import Clipboard_conn, ConnectionThread

class Client():
    def __init__(self, server_url='http://localhost'):
        self.conn = Clipboard_conn(server_url)
        self.window = self.render_gui()

    def render_gui(self):
        window = tk.Tk()
        window.title('ClipboardOTA')

        title_label = tk.Label(window, text='Clipboard Over The Air')
        title_label.grid(column=1, row=0, padx=5, pady=5)

        url_box = tk.Text(window, height=1, width=50)
        url_box.grid(column=1, row=1, padx=5, pady=5)

        get_button = tk.Button(window, text='Get clipboard', command=self.get_clipboard)
        get_button.grid(column=0, row=2, padx=5, pady=5)

        post_button = tk.Button(window, text='Send clipboard', command=self.post_wrapper)
        post_button.grid(column=1, row=2, padx=5, pady=5)

        del_button = tk.Button(window, text='Delete clipboard', command=self.delete_clipboard)
        del_button.grid(column=2, row=2, padx=5, pady=5)

        debug_clipboard_box = tk.Text(window, height=20, width=50)
        debug_clipboard_box.grid(column=1, row=3, padx=5, pady=5)

        return window

    def request_handler(self):
        pass

    def thread_manager(self, thread):
        pass