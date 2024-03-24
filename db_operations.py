import sqlite3
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

class dbOperation:
    def __init__(self, db_file="passwords.db"):
        self.db_file = db_file
        self.conn = self.connect()
        self.cur = self.conn.cursor()
        self.create_table()

    def connect(self):
        return sqlite3.connect(self.db_file)

    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """
        self.conn.execute(query)
        self.conn.commit()

    def dbSaveEntry(self, data):
        query = (
            f"""INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)"""
        )
        encryptedpass = hash_password(data["password"])
        self.conn.execute(query, (data["website"], data["username"], encryptedpass))
        self.conn.commit()

    def dbGetAllEntry(self):
        query = "SELECT * FROM passwords"
        entry = self.conn.execute(query)
        return entry

    def dbUpdateEntry(self, data):
        query = (
            "UPDATE passwords SET website = ?, username = ?, password = ? WHERE id = ?"
        )
        encryptedpass = hash_password(data["password"])
        self.conn.execute(
            query, (data["website"], data["username"], encryptedpass , data["ID"])
        )
        self.conn.commit()

    def dbDelEntry(self, id):
        query = "DELETE FROM passwords WHERE id = ?"
        self.conn.execute(query, (id,))
        self.conn.commit()

    def search_entry(self, search_term):
        query = """
            SELECT * FROM passwords
            WHERE website LIKE ? OR username LIKE ?
        """
        self.cur.execute(query, (f"%{search_term}%", f"%{search_term}%"))
        return self.cur.fetchall()
