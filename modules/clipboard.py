from tkinter import TclError
import logging

def insert_text(window, text):
    window.clipboard_clear()
    window.clipboard_append(text)
    window.update()

def get_text(window):
    try:
        return window.clipboard_get()
    except TclError:
        logging.debug('Getting clipboard contents failed, replacing with empty string')
        return ''