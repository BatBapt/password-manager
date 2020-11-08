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
        label_inline = tk.Label(self.line_frame, text="test depuis CSV")
        label_inline.pack(side=tk.TOP, padx=(210, 0))

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

    def add_in_database(self, values):
        if self.is_good:
            for row in values:
                row.insert(0, self.username)
                self.database.add_row(row)



