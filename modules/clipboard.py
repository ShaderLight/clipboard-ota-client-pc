def insert_text(window, text):
    window.clipboard_clear()
    window.clipboard_append(text)
    window.update()

def get_text(window):
    return window.clipboard_get()