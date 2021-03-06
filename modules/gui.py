import pystray

import tkinter as tk
import tkinter.ttk as ttk
import logging
import os
from PIL import Image, ImageTk


from .server_requests import Clipboard_conn, ConnectionThread
from .clipboard import insert_text, get_text

class Client():
    def __init__(self, server_url='http://localhost:9009'):
        self.conn = Clipboard_conn(server_url)
        self.buttons_enabled = True
        self.window = self.render_gui()
        self.render_menu()
        self.icon_image=Image.open('favicon.png')

        self.window.protocol('WM_DELETE_WINDOW', self.hide_to_tray)
        self.window.iconphoto(True, tk.PhotoImage(file='favicon.png'))

    def render_gui(self):
        window = tk.Tk()
        window.title('ClipboardOTA')                                                                                                    

        title_label = tk.Label(window, text='Clipboard Over The Air')
        title_label.grid(column=1, row=0, padx=5, pady=5)

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

    def render_menu(self):
        self.menu_bar = tk.Menu(self.window)
        self.settings_menu = tk.Menu(self.menu_bar)
        self.help_menu = tk.Menu(self.menu_bar)

        self.settings_menu.add_command(label='Sync')
        self.settings_menu.add_command(label='Server', command=self.render_server_window)

        self.help_menu.add_command(label='About ClipboardOTA', command=self.render_about_window)
        self.help_menu.add_command(label='GitHub repo', command=self.open_gh_page)

        self.menu_bar.add_cascade(label='Settings', menu=self.settings_menu)
        self.menu_bar.add_cascade(label='Help', menu=self.help_menu)

        self.window.config(menu=self.menu_bar)

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

    def open_gh_page(self):
        os.system("start \"\" https://github.com/ShaderLight/clipboard-ota-client-pc")

    def render_about_window(self, width=400, height=200):
        about_window = tk.Toplevel(self.window)
        title_label = tk.Label(about_window, text='Clipboard Over The Air\n v0.0.1\nby ShaderLight\n under MIT License')
        title_label.grid(column=1, row=0, padx=5, pady=5)

        about_window.title('About Clipboard OTA')
        about_window.geometry(f"{width}x{height}+{self.window.winfo_x() + int((self.window.winfo_width()-width)/2)}+{self.window.winfo_y() + int((self.window.winfo_height()-height)/2)}")

    def render_sync_window(self, width=400, height=400):
        sync_window = tk.Toplevel(self.window)
        title_label = tk.Label(sync_window, text='Sync settings')

        sync_window.title('Sync settings')
        sync_window.geometry(f"{width}x{height}+{self.window.winfo_x() + int((self.window.winfo_width()-width)/2)}+{self.window.winfo_y() + int((self.window.winfo_height()-height)/2)}")

    def render_server_window(self, width=400, height=400):
        server_window = tk.Toplevel(self.window)
        title_label = tk.Label(server_window, text='Server URL')
        title_label.pack(padx=5, pady=5)

        url_box = tk.Entry(server_window)
        url_box.insert(tk.END, self.conn.resource_url)
        url_box.pack(padx=5, pady=5, fill='both')

        change_url_button = tk.Button(server_window, text='Change URL')
        change_url_button.pack(padx=5, pady=5)

        server_window.title('Server settings')
        server_window.geometry(f"{width}x{height}+{self.window.winfo_x() + int((self.window.winfo_width()-width)/2)}+{self.window.winfo_y() + int((self.window.winfo_height()-height)/2)}")

    def hide_to_tray(self):
        self.window.withdraw()
        menu = (pystray.MenuItem('Show', self.show_window, default=True), pystray.MenuItem('Close', self.terminate))
        icon = pystray.Icon('name', self.icon_image, 'ClipboardOTA', menu)
        icon.run()

    def terminate(self, icon, item):
        icon.stop()
        self.window.destroy()

    def show_window(self, icon, item):
        icon.stop()
        self.window.after(0, self.window.deiconify())
