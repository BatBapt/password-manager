import sqlite3
import bcrypt
from datetime import datetime


class Database:
    database_name = ""
    def __init__(self, database_name):
        self.database_name = database_name
        try:
            self.conn = sqlite3.connect(self.database_name)
            self.cur = conn.cursor()
            print("Connecté à la base de donnée")
        except sqlite3.Error as error:
            print("Erreur lors de la connection à la base de donnée: {}".format(error)) 
        
        self.init_table_password()

    def init_table_password(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS password(
                id INTEGER PRIMARY KEY,
                app VARCHAR(100) NOT NULL,
                added_date DATETIME NOT NULL,
                pseudo VARCHAR(100) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
            """
        )
    
    def add_row_password(self, values):
        sql = """INSERT INTO password(app, added_date, pseudo, password) VALUES(?, ?, ?, ?)"""
        self.cur.execute(sql, values)
        self.conn.commit()

        return self.cur.lastrowid

if __name__ == '__main__':
    file = "password.db"
    database = Database(file)
    database.add_row_password(['gmail', datetime.now(), "baptou", "1234"])
