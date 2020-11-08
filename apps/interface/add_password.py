import tkinter as tk
from tkinter import filedialog

import csv

import apps.interface.home as home
from apps.database import database


class AddPassword(tk.Frame):
    username = ""
    csv_file = ""
    column_name = []
    is_good = False

    def __init__(self, master, username):
        tk.Frame.__init__(self, master)

        self.master = master
        self.username = username

        self.database = database.Database("password.db")

        self.master.title("Password Manager: Ajouter des Mots de passe")
        self.master.geometry("900x450+300+100")

        self.frame = tk.Frame(self.master, width=900, height=450)
        self.frame.pack()

        home_btn = tk.Button(self.frame, text="Accueil", command=self.back_home)
        home_btn.pack(side=tk.TOP)

        self.csv_frame = tk.Frame(self.frame, width=450, height=450)
        self.csv_frame.pack(side=tk.LEFT, fill=tk.X)

        self.line_frame = tk.Frame(self.frame, width=450, height=450)
        self.line_frame.pack()

        self.file_state = tk.Label(self.csv_frame, text="")
        self.line_state = tk.Label(self.line_frame, text="")

        self.entry_app = tk.Entry(self.line_frame)
        self.entry_user = tk.Entry(self.line_frame)
        self.entry_pwd = tk.Entry(self.line_frame, show="*")

        self.gen_csv()
        self.gen_inline()

    def back_home(self):
        self.frame.destroy()
        home.Home(self.master, self.username)

    def gen_csv(self):
        label_csv = tk.Label(self.csv_frame, text="Importer depuis CSV")
        label_csv.pack(side=tk.TOP, padx=(0, 210))

        tk.Label(self.csv_frame, text="Assurez vous que le fichier soit de la forme: name/url/pseudo/password")\
            .pack(side=tk.TOP, padx=(0, 210))

        csv_btn = tk.Button(self.csv_frame, text="Ouvrir un fichier csv", command=self.open_file)
        csv_btn.pack(side=tk.TOP, padx=(0, 210), pady=(50, 0))

        self.file_state.pack(side=tk.TOP, padx=(0, 210), pady=(20, 0))

    def gen_inline(self):
        label_inline = tk.Label(self.line_frame, text="Entrer à la main")
        label_inline.pack(side=tk.TOP, padx=(0, 150))

        label_app = tk.Label(self.line_frame, text="Application: ")
        label_app.pack(side=tk.TOP, padx=(0, 150), pady=(20, 0))

        self.entry_app.pack(side=tk.TOP, padx=(0, 150))

        label_user = tk.Label(self.line_frame, text="Pseudo: ")
        label_user.pack(side=tk.TOP, padx=(0, 150), pady=(20, 0))

        self.entry_user.pack(side=tk.TOP, padx=(0, 150))

        label_pwd = tk.Label(self.line_frame, text="Mot de passe: ")
        label_pwd.pack(side=tk.TOP, padx=(0, 150), pady=(20, 0))

        self.entry_pwd.pack(side=tk.TOP, padx=(0, 150))

        btn = tk.Button(self.line_frame, text="Enregistrer le mot de passe", width=40, command=lambda: self.treatment(
            app=self.entry_app,
            name=self.entry_user,
            pwd=self.entry_pwd,
        ))
        btn.pack(side=tk.TOP, padx=(0, 150), pady=(20, 20))

        self.line_frame.bind_all('<Return>', lambda event: self.treatment(
            app=self.entry_app,
            name=self.entry_user,
            pwd=self.entry_pwd,
        ))

    def treatment(self, event=None, **kwargs):
        app = kwargs['app'].get()
        name = kwargs['name'].get()
        pwd = kwargs['pwd'].get()

        if len(app) > 0 and len(name) > 0 and len(pwd) > 0:
            self.is_good = True
            values = [self.username, app, name, pwd]

            self.add_in_database(values, is_csv=False)
        else:
            self.line_state["text"] = "Un champ est manquant"
            self.line_state.pack(side=tk.TOP, padx=(0, 150), pady=(20, 20))

    def open_file(self):
        self.csv_file = tk.filedialog.askopenfilename(initialdir="/", title="Ouvrir CSV", filetypes=(("CSV Files","*.csv"),))

        with open(self.csv_file, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            self.column_name = next(reader)

            data = list(reader)

            for i in range(len(data)):
                del data[i][0]

            if 'url' in self.column_name and 'username' in self.column_name and 'password' in self.column_name:
                self.is_good = True
                self.file_state.configure(text="Fichier importé: {}".format(self.csv_file))
                self.add_in_database(data)
            else:
                self.file_state.configure(text="Erreur lors de l'import: les colonnes ont un mauvais nom")

    def add_in_database(self, values, is_csv=True):
        if self.is_good:
            if is_csv:
                for row in values:
                    row.insert(0, self.username)
                    self.database.add_row(row)

                    self.file_state.configure(text="Les lignes ont été importée correctement")
            else:
                self.database.add_row(values)
                self.line_state.configure(text="Mot de passe enregistrée")
                self.line_state.pack(side=tk.TOP, padx=(0, 150), pady=(20, 20))

                self.entry_app.delete(0, 'end')
                self.entry_user.delete(0, 'end')
                self.entry_pwd.delete(0, 'end')



if __name__ == '__main__':
    root = tk.Tk()
    app = AddPassword(root, 'Baptiste')
    app.mainloop()