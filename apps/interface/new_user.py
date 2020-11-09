import tkinter as tk
from tkinter import messagebox

from apps.database import database
import apps.interface.login as login


class NewUser(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.database = database.Database("password.db")

        for widget in self.master.winfo_children():
            widget.destroy()

        self.master.title("Password Manager: Créer un compte")
        self.master.geometry("900x450+300+100")

        self.main_frame = tk.Frame(self.master, width=900, height=450)
        self.main_frame.pack()

        self.error_lab = tk.Label(self.master, text="")

        self.gen_form()

    def gen_form(self):
        user_str = tk.StringVar()
        pwd_str = tk.StringVar()

        tk.Label(self.main_frame, text="Nom d'utilisateur: ").pack(side=tk.TOP, pady=(25, 0))

        tk.Entry(self.main_frame, width=30, textvariable=user_str).pack(side=tk.TOP)

        tk.Label(self.main_frame, text="Mot de passe: ").pack(side=tk.TOP, pady=(25, 0))

        tk.Entry(self.main_frame, show="*", width=30, textvariable=pwd_str).pack(side=tk.TOP)

        btn = tk.Button(self.main_frame, text="S'inscrire", width=45, command=lambda: self.signup(
            user=user_str,
            pwd=pwd_str,
        ))
        btn.pack(side=tk.TOP, pady=(30, 30))

        self.main_frame.bind_all('<Return>', lambda event: self.signup(
            user=user_str,
            pwd=pwd_str,
        ))

    def signup(self, event=None, **kwargs):
        user = kwargs["user"].get()
        pwd = kwargs["pwd"].get()

        if len(user) > 0 and len(pwd) > 0:
            self.database.add_user([user, pwd])
            messagebox.showinfo("Inscription réussis", "Votre inscription est enregistré. Veuillez vous connecter")
            login.Login(self.master)
        else:
            self.error_lab["text"] = "Un des champs est manquant"
            self.error_lab.pack(side=tk.TOP)


if __name__ == "__main__":
    root = tk.Tk()
    app = NewUser(root)
    app.mainloop()