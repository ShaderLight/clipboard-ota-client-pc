import tkinter as tk
import tkinter.ttk as ttk


class Client:
    def __init__(self):
        pass

    def render_gui(self, conn):
        window = tk.Tk()
        window.title('ClipboardOTA')

        title_label = tk.Label(window, text='Clipboard Over The Air')
        title_label.grid(column=1, row=0, padx=5, pady=5)

        url_box = tk.Text(window, height=1, width=50)
        url_box.grid(column=1, row=1, padx=5, pady=5)

        get_button = tk.Button(window, text='Get clipboard', command=conn.get_clipboard)
        get_button.grid(column=0, row=2, padx=5, pady=5)

        post_button = tk.Button(window, text='Send clipboard', command=self.post_wrapper)
        post_button.grid(column=1, row=2, padx=5, pady=5)

        del_button = tk.Button(window, text='Delete clipboard', command=conn.delete_clipboard)
        del_button.grid(column=2, row=2, padx=5, pady=5)

        debug_clipboard_box = tk.Text(window, height=20, width=50)
        debug_clipboard_box.grid(column=1, row=3, padx=5, pady=5)

        window.mainloop()

    def post_wrapper():
        pass