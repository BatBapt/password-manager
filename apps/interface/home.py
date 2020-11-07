import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from apps.database import database

import apps.interface.login as login
import apps.interface.add_password as add_password


class Home(tk.Frame):
    username = ""
    pseudo = ""

    def __init__(self, master, username):
        self.master = master

        self.username = username
        self.database = database.Database("../password.db")
        self.username = self.database.print_by_user(self.username)
        self.pseudo = self.username[1]

        tk.Frame.__init__(self, master)

        self.master.title("Password Manager: Home")
        self.master.geometry("900x450+300+100")

        self.main_frame = tk.Frame(self.master, width=900, height=150)
        self.img_frame = tk.Frame(self.master, width=900, height=300)

        self.main_frame.place(rely=0, relheight=0.5, relwidth=1)
        self.img_frame.place(rely=0.5, relheight=0.5, relwidth=1)

        self.add_canv = tk.Canvas(self.img_frame, width=300, height=300)
        self.add_canv.pack(side=tk.LEFT)

        self.list_canv = tk.Canvas(self.img_frame, width=300, height=300)
        self.list_canv.pack(side=tk.LEFT)

        self.search_canv = tk.Canvas(self.img_frame, width=300, height=300)
        self.search_canv.pack(side=tk.LEFT)

        self.gen_main()
        self.gen_btn()
        self.gen_icon()

    def gen_main(self):
        dc_btn = tk.Button(self.main_frame, text="Se déconnecter", command=self.deconnect)
        dc_btn.pack(anchor="e")

        info_label = tk.Label(self.main_frame, text="Bienvenu à toi {}".format(self.pseudo))
        info_label.pack(pady=(40, 0))
        tk.Label(self.main_frame, text="Que veux-tu faire? ").pack()

    def gen_icon(self):

        img_list = ['add.png', 'list.png', 'loupe.png']
        canvas_list = [self.add_canv, self.list_canv, self.search_canv]

        for i in range(3):
            img = Image.open("../../assets/" + img_list[i])
            img = img.resize((300, 250), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            canvas_list[i].create_image(0, 0, anchor=tk.NW, image=photo)
            canvas_list[i].image = photo

    def gen_btn(self):
        btn_list = ['Ajouter mot de passe', 'Lister les mots de passe', 'Chercher un mot de passe']
        btn_command_list = [
            lambda: self.add_password(master_root=self.master, user=self.pseudo),
            self.master.destroy,
            self.master.destroy
        ]
        tmp_list = []
        aux = 100

        for i in range(3):
            tmp_list.append(tk.Button(self.main_frame, text=btn_list[i], command=btn_command_list[i], width=30))
            tmp_list[i].pack(side=tk.LEFT, padx=45)

    def deconnect(self):
        msg_box = messagebox.askquestion('Déconnection', 'Êtes-vous sur de vous déconnecter?', icon='warning')
        if msg_box == "yes":
            self.main_frame.destroy()
            self.img_frame.destroy()
            login.Login(self.master)

    def add_password(self, **kwargs):
        master_root = kwargs["master_root"]
        user = kwargs["user"]
        self.main_frame.destroy()
        self.img_frame.destroy()
        add_password.AddPassword(master_root, user)

