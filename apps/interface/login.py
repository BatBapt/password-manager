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
        user_str = tk.StringVar()
        pwd_str = tk.StringVar()

        info_label = tk.Label(self.login_frame, text="Vous devez vous connecter pour voir vos mots de passe")
        info_label.pack(padx=5, pady=15, side=tk.TOP)

        tk.Label(self.login_frame, text="Nom d'utilisateur").pack(pady=0)
        tk.Entry(self.login_frame, width=50, textvariable=user_str).pack(ipady=2, pady=10)

        tk.Label(self.login_frame, text="Mot de passe").pack(pady=10)
        tk.Entry(self.login_frame, width=50, show="*", textvariable=pwd_str).pack(ipady=2, pady=10)

        connect_button = tk.Button(self.login_frame, text="Se connecter", command=lambda: self.connect(
            user=user_str, pwd=pwd_str
        ))
        connect_button.pack()
        self.login_frame.bind_all("<Return>", lambda event: self.connect(user=user_str, pwd=pwd_str))

    def connect(self, event=None, **kwargs):
        user = kwargs["user"].get()
        pwd = kwargs["pwd"].get()

        is_connected = self.database.connection_user(user, pwd)
        if is_connected:
            self.login_frame.destroy()
            home.Home(self.master, user)

    def create_user(self):
        new.NewUser(self.master)

