import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

import apps.interface.home as home
from apps.database import database


class ListPassword(tk.Frame):
    tab = None

    def __init__(self, master, username):
        tk.Frame.__init__(self, master)

        self.master = master
        for widget in self.master.winfo_children():
            widget.destroy()

        self.username = username

        self.database = database.Database("../password.db")
        self.master.title("Password Manager: Lister les mots de passe")
        self.master.geometry("900x450+300+100")

        self.frame = tk.Frame(self.master, width=900, height=450)
        self.frame.pack()

        home_btn = tk.Button(self.frame, text="Accueil", command=self.back_home)
        home_btn.pack(side=tk.TOP)

        self.site_label = tk.Label(self.frame, text="")
        self.pseudo_label = tk.Label(self.frame, text="")
        self.password_label = tk.Label(self.frame, text="")

        self.gen_info()
        self.gen_tree_view()

    def back_home(self):
        self.frame.destroy()
        print(self.username)
        home.Home(self.master, self.username)

    def gen_info(self):
        tk.Label(self.frame, text='Quelques informations sur le tableau:').pack(side=tk.TOP)
        tk.Label(self.frame, text="1- Pour accéder aux informations d'une ligne, appuyez sur 'Entrer' en la "
                                  "selectionnant").pack(side=tk.TOP)
        tk.Label(self.frame, text="2- Pour supprimer une ligne, appuyez sur 'Suppr' en la selectionnant")\
            .pack(side=tk.TOP)

    def gen_tree_view(self):
        self.tab = ttk.Treeview(self.frame, columns=('site', 'pseudo', 'password'))
        self.tab.heading('site', text='Url du site')
        self.tab.column('site', minwidth=0, width=300, stretch=tk.NO)
        self.tab.heading('pseudo', text='Pseudo du compte du site')
        self.tab.column('pseudo', minwidth=0, width=250, stretch=tk.NO)
        self.tab.heading('password', text='Mot de passe du compte du site')
        self.tab.column('password', minwidth=0, width=350, stretch=tk.NO)
        self.tab['show'] = 'headings'
        self.tab.pack(expand=tk.YES, fill=tk.BOTH)
        
        rows = self.database.print_row(self.username)
        if rows:
            for row in rows:
                self.tab.insert('', 'end', iid=row[0], values=(row[2], row[3], row[4]))

        self.tab.bind('<Return>', self.select_row)
        self.tab.bind('<Delete>', self.delete_row)

    def select_row(self, event):
        row_id = self.tab.focus()
        row = self.database.print_row_by_id(row_id)

        self.site_label.configure(text="URL {}".format(row[2]))
        self.pseudo_label.configure(text="PSEUDO: {}".format(row[3]))
        self.password_label.configure(text="MOT DE PASSE: {}".format(row[4]))

        self.site_label.pack()
        self.pseudo_label.pack()
        self.password_label.pack()

    def delete_row(self, event):
        row_id = self.tab.focus()
        msg_box = messagebox.askquestion('Suppression', 'Êtes-vous sur de supprimer la ligne {}?'.format(row_id), 
                                         icon='warning')
        if msg_box == "yes":
            self.database.delete_row(row_id)
            self.refresh()

    def refresh(self):
        self.__init__(self.master, self.username)

