import tkinter as tk
import tkinter.ttk as ttk
import logging

from .server_requests import Clipboard_conn, ConnectionThread
from .clipboard import insert_text, get_text

class Client():
    def __init__(self, server_url='http://localhost:9009'):
        self.conn = Clipboard_conn(server_url)
        self.buttons_enabled = True
        self.window = self.render_gui()

    def render_gui(self):
        window = tk.Tk()
        window.title('ClipboardOTA')                                                                                                    

        title_label = tk.Label(window, text='Clipboard Over The Air')
        title_label.grid(column=1, row=0, padx=5, pady=5)

        url_box = tk.Text(window, height=1, width=50)
        url_box.grid(column=1, row=1, padx=5, pady=5)

        self.get_button = tk.Button(window, text='Get clipboard', command=lambda: self.request_handler('get'))
        self.get_button.grid(column=0, row=2, padx=5, pady=5)

        self.post_button = tk.Button(window, text='Send clipboard', command=lambda: self.request_handler('post'))
        self.post_button.grid(column=1, row=2, padx=5, pady=5)

        self.del_button = tk.Button(window, text='Delete clipboard', command=lambda: self.request_handler('delete'))
        self.del_button.grid(column=2, row=2, padx=5, pady=5)

        self.debug_clipboard_box = tk.Text(window, height=20, width=50)
        self.debug_clipboard_box.grid(column=1, row=3, padx=5, pady=5)

        self.button_list = [self.get_button, self.post_button, self.del_button]

        return window

    def request_handler(self, method):
        self.toggle_buttons()
        if method == 'post':
            text = get_text(self.window)
            thread = ConnectionThread(self.conn, method, text)
        else:
            thread = ConnectionThread(self.conn, method)
        
        thread.start()

        self.thread_manager(thread)

    def thread_manager(self, thread):
        if thread.is_alive():
            self.window.after(100, lambda: self.thread_manager(thread))
        else:
            self.toggle_buttons()
            logging.debug(thread.response)
            logging.debug('Received content with text "{}" and timestamp "{}"'.format(thread.response['text'], thread.response['timestamp']))
            insert_text(self.window, thread.response['text'])
            self.debug_clipboard_box.delete(1.0, tk.END) # Without deleting first, the text would just append to the previous output
            self.debug_clipboard_box.insert(tk.END, thread.response['text'])

    def toggle_buttons(self):
        if self.buttons_enabled:
            for button in self.button_list:
                button.configure(state='disabled')
            self.buttons_enabled = False
        else:
            for button in self.button_list:
                button.configure(state='normal')
            self.buttons_enabled = True
