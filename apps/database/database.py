import sqlite3
import bcrypt
from datetime import datetime


class Database:

    def __init__(self, database_name):
        self.database_name = database_name
        try:
            self.conn = sqlite3.connect(self.database_name)
            self.cur = self.conn.cursor()
        except sqlite3.Error as error:
            print("Erreur lors de la connection à la base de donnée: {}".format(error))

        self.init_table_password()

    def init_table_password(self):
        """

        :return:
        """
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            password VARCHAR(255) NOT NULL,
            signup_date DATETIME NOT NULL
            )
            """
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS password(
                id INTEGER PRIMARY KEY,
                username VARCHAR(100) NOT NULL,
                app VARCHAR(255) NOT NULL,
                pseudo VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                
                FOREIGN KEY (username) REFERENCES users(username)
            )
            """
        )

    def add_user(self, values):
        salt = bcrypt.gensalt()
        values[1] = bcrypt.hashpw(bytes(values[1], encoding='ascii'), salt)
        values.append(datetime.now())
        sql = "INSERT INTO users(username, password, signup_date) VALUES(?, ?, ?)"
        self.cur.execute(sql, values)
        self.conn.commit()

    def add_row(self, values):
        """
        :param values:  list of values to add in the db:
        values[0] => username logged
        values[1] => app name
        values[2] => pseudo for the app
        values[3] => password for the app
        values[4] => datetime // Added in this function
        :return: the id of the row added
        """
        sql = "INSERT INTO password(username, app, pseudo, password) VALUES(?, ?, ?, ?)"
        self.cur.execute(sql, values)
        self.conn.commit()  # store and save the row in the database
        print("Ligne enregistrée")
        return self.cur.lastrowid

    def connection_user(self, username, pwd):
        sql = "SELECT * FROM users WHERE username=?"
        self.cur.execute(sql, (username, ))
        row = self.cur.fetchone()
        if row is not None:
            password = row[2]
            if bcrypt.checkpw(bytes(pwd, encoding='ascii'), password):
                return True
            else:
                return False
        else:
            return False

    def print_by_user(self, user):
        sql = "SELECT * FROM users WHERE username=?"
        self.cur.execute(sql, (user, ))
        row = self.cur.fetchone()
        if row is not None:
            return row
        else:
            return False
        
    def print_row(self, username):
        sql = "SELECT * FROM password WHERE username=?"
        self.cur.execute(sql, (username, ))

        rows = self.cur.fetchall()
        if rows is not None:
            return rows
        else:
            return False

    def print_row_by_id(self, ids):
        sql = "SELECT * FROM password WHERE id=?"
        self.cur.execute(sql, (ids, ))
        row = self.cur.fetchone()
        return row

    def update_row(self, ids, pseudo="", password=""):
        """

        :param ids: if of the row to update
        :param pseudo: pseudo to update
        :param password: password to update
        :return:
        """
        if len(pseudo) == 0 and len(password) > 0:
            sql = "UPDATE password set password=? WHERE id=?"
            self.cur.execute(sql, (password, ids, ))
        elif len(pseudo) > 0 and len(password) == 0:
            sql = "UPDATE password set pseudo=? WHERE id=?"
            self.cur.execute(sql, (pseudo, ids,))
        elif len(pseudo) > 0 and len(password) > 0:
            sql = "UPDATE password set pseudo=? AND password=? WHERE id=?"
            self.cur.execute(sql, (pseudo, password, ids,))
        self.conn.commit()
        print("Ligne modifiée correctement.")

    def delete_row(self, ids):
        """

        :param ids: id to delete
        :return:
        """
        sql = "DELETE FROM password WHERE id=?"
        self.cur.execute(sql, (ids,))
        self.conn.commit()
        print("Lignée supprimée correctement")

