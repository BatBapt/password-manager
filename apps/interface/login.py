import tkinter as tk

from apps.database import database

import apps.interface.home as home
import apps.interface.new_user as new


class Login(tk.Frame):

    def __init__(self, master):
        self.database = database.Database("password.db")

        self.master = master
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Frame.__init__(self, master)

        self.master.title("Password Manager: Login")
        self.master.geometry("900x450+300+100")

        self.login_frame = tk.Frame(self.master, width=900, height=200)
        self.login_frame.pack(side=tk.TOP, fill=tk.X)

        self.signup_frame = tk.Frame(self.master, width=900, height=250)
        self.signup_frame.pack(fill=tk.X)

        tk.Button(self.signup_frame, text="Enregistrer un compte", width=30, command=self.create_user).pack(pady=(75, 0))

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
        self.login_frame.bind_all("<Return>", lambda event: self.connect(user=user_entry, pwd=pwd_entry))

    def connect(self, event=None, **kwargs):
        user = kwargs["user"].get()
        pwd = kwargs["pwd"].get()

        is_connected = self.database.connection_user(user, pwd)
        if is_connected:
            self.login_frame.destroy()
            home.Home(self.master, user)

    def create_user(self):
        new.NewUser(self.master)

