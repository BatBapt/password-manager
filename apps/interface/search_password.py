import tkinter as tk
import tkinter.ttk as ttk

import apps.interface.home as home
from apps.database import database


class SearchPassword(tk.Frame):
    app_entry = None
    pseudo_entry = None

    def __init__(self, master, username):
        tk.Frame.__init__(self, master)

        self.master = master
        for widget in self.master.winfo_children():
            widget.destroy()
        self.username = username
        self.database = database.Database("password.db")

        self.master.title("Password Manager: Chercher un mot de passe")
        self.master.geometry("900x450+300+100")

        self.frame = tk.Frame(self.master, width=900, height=450)
        self.frame.pack()

        home_btn = tk.Button(self.frame, text="Accueil", command=self.back_home)
        home_btn.pack(side=tk.TOP)

        self.app_frame = tk.Frame(self.frame, width=450, height=250)
        self.app_frame.pack(side=tk.LEFT, fill=tk.X)

        self.user_frame = tk.Frame(self.frame, width=450, height=250)
        self.user_frame.pack(side=tk.RIGHT)

        self.result_frame = tk.Frame(self.master, width=900, height=200)
        self.result_frame.pack()

        self.result_label = tk.Label(self.result_frame)

        self.frame.bind_all('<Return>', self.search)

        self.gen_form_search_by_app()
        self.gen_form_search_by_user()

    def back_home(self):
        self.frame.destroy()
        home.Home(self.master, self.username)

    def gen_form_search_by_app(self):
        tk.Label(self.app_frame, text="Entrez un site: ").pack(side=tk.TOP, pady=(20, 0), padx=(0, 225))

        self.app_entry = tk.Entry(self.app_frame, width=30)
        self.app_entry.pack(side=tk.TOP, padx=(0, 225))

        btn_app = tk.Button(self.app_frame, text="Chercher", width=20, command=self.search)
        btn_app.pack(side=tk.TOP, padx=(0, 225))

    def gen_form_search_by_user(self):
        tk.Label(self.user_frame, text="Entrez un pseudo: ").pack(side=tk.TOP, pady=(20, 0), padx=(100, 0))

        self.pseudo_entry = tk.Entry(self.user_frame, width=30)
        self.pseudo_entry.pack(side=tk.TOP, padx=(100, 0))

        btn_pseudo = tk.Button(self.user_frame, text="Chercher", width=20, command=self.search)
        btn_pseudo.pack(side=tk.TOP, padx=(100, 0))

    def search(self, event=None):
        rows = None
        app = self.app_entry.get()
        pseudo = self.pseudo_entry.get()

        if len(app) == 0 and len(pseudo) > 0:

            rows = self.database.search_by_pseudo(pseudo)
        elif len(pseudo) == 0 and len(app) > 0:
            rows = self.database.search_by_app(app)
        else:
            rows = None

        self.app_entry.delete(0, 'end')
        self.pseudo_entry.delete(0, 'end')
        self.display_result(rows)

    def display_result(self, rows):

        for widget in self.result_frame.winfo_children():
            if widget.winfo_class() != "Label":
                widget.destroy()
            else:
                self.result_label["text"] = ""

        if rows is not None and len(rows) > 0:
            tab = ttk.Treeview(self.result_frame, columns=('site', 'pseudo', 'password'))
            tab.heading('site', text='Url du site')
            tab.column('site', minwidth=0, width=300, stretch=tk.NO)
            tab.heading('pseudo', text='Pseudo du compte du site')
            tab.column('pseudo', minwidth=0, width=250, stretch=tk.NO)
            tab.heading('password', text='Mot de passe du compte du site')
            tab.column('password', minwidth=0, width=350, stretch=tk.NO)
            tab['show'] = 'headings'
            tab.pack(expand=tk.YES, fill=tk.BOTH)

            for row in rows:
                tab.insert('', 'end', iid=row[0], values=(row[2], row[3], row[4]))

        else:
            self.result_label["text"] = "Pas de résultat trouvé."
            self.result_label.pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = SearchPassword(root, 'Baptiste')
    app.mainloop()

