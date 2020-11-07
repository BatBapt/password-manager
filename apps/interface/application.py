import tkinter as tk

from apps.interface.login import Login


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        Login(self)


if __name__ == '__main__':
    app = Application()
    app.mainloop()
    exit(1)
