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

        self.username_entry = tk.Entry(self.main_frame)
        self.password_entry = tk.Entry(self.main_frame, show="*")

        self.gen_form()

    def gen_form(self):
        username_label = tk.Label(self.main_frame, text="Nom d'utilisateur: ")
        username_label.pack(side=tk.TOP, pady=(25, 0))

        self.username_entry["width"] = 30
        self.username_entry.pack(side=tk.TOP)

        password_label = tk.Label(self.main_frame, text="Mot de passe: ")
        password_label.pack(side=tk.TOP, pady=(25, 0))

        self.password_entry['width'] = 30
        self.password_entry.pack(side=tk.TOP)

        btn = tk.Button(self.main_frame, text="S'inscrire", width=45, command=lambda: self.signup(
            user=self.username_entry,
            pwd=self.password_entry,
        ))
        btn.pack(side=tk.TOP, pady=(30, 30))

        self.main_frame.bind_all('<Return>', lambda event: self.signup(
            user=self.username_entry,
            pwd=self.password_entry,
        ))

    def signup(self, event=None, **kwargs):
        user = kwargs["user"].get()
        pwd = kwargs["pwd"].get()

        if len(user) > 0 and len(pwd) > 0:
            self.database.add_user([user, pwd])
            messagebox.showinfo("Inscription réussis", "Votre inscription est enregistré. Veuillez vous connecter")
            login.Login(self.master)






if __name__ == "__main__":
    root = tk.Tk()
    app = NewUser(root)
    app.mainloop()