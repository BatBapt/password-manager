import tkinter as tk

from apps.database import database


class Application(tk.Tk):
    def __init__(self):

        self.database = database.Database("../password.db")

        tk.Tk.__init__(self)
        self.geometry("900x600+300+100")
        self.title("Password Manager")

        self.login_frame = tk.Frame(self, width=900, height=450)
        self.login_frame.pack()

        self.login_window()

    def login_window(self):
        info_label = tk.Label(self.login_frame, text="Vous devez vous connecter pour voir vos mots de passe")
        info_label.pack(padx=5, pady=15, side=tk.TOP)

        user_label = tk.Label(self.login_frame, text="Nom d'utilisateur")
        user_label.pack(pady=0)
        user_entry = tk.Entry(self.login_frame, width=50)
        user_entry.pack(ipady=2, pady=10)

        pwd_label = tk.Label(self.login_frame, text="Mot de passe")
        pwd_label.pack(pady=10)
        pwd_entry = tk.Entry(self.login_frame, width=50, show="*")
        pwd_entry.pack(ipady=2, pady=10)

        connect_button = tk.Button(self.login_frame, text="Se connecter", command=lambda: self.connect(
            user=user_entry, pwd=pwd_entry
        ))
        connect_button.pack()

    def connect(self, **kwargs):
        user = kwargs["user"].get()
        pwd = kwargs["pwd"].get()
        is_connected = self.database.connection_user(user, pwd)

        if is_connected:
            self.login_frame.destroy()


if __name__ == '__main__':
    app = Application()
    app.mainloop()
