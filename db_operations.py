import sqlite3

import bcrypt
from cryptography.fernet import Fernet


def generate_key(password):
    key = bcrypt.kdf(
        password=password.encode(), salt=b"salt", desired_key_bytes=32, rounds=100
    )
    return key


def encrypt_password(password):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    ciphered_text = cipher_suite.encrypt(password.encode())
    return ciphered_text


def decrypt_password(self, encrypted_password):
    decrypted_password = self.fernet.decrypt(encrypted_password).decode()
    return decrypted_password


class dbOperation:
    def __init__(self, masterpassword):
        self.db_file = "passwords.db"
        self.conn = self.connect()
        self.cur = self.conn.cursor()
        self.create_table()
        generate_key(masterpassword)

    def connect(self):
        return sqlite3.connect(self.db_file)

    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS user_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """
        self.conn.execute(query)
        self.conn.commit()

    def dbSaveEntry(self, data):
        query = f"""INSERT INTO user_accounts (website, username, password) VALUES (?, ?, ?)"""
        encryptedpass = encrypt_password(data["password"])
        self.conn.execute(query, (data["website"], data["username"], encryptedpass))
        self.conn.commit()

        self.conn.commit()

    def dbGetAllEntry(self):
        query = "SELECT * FROM user_accounts"
        entry = self.conn.execute(query)
        return entry

    def dbUpdateEntry(self, data):
        query = "UPDATE user_accounts SET website = ?, username = ?, password = ? WHERE id = ?"
        encryptedpass = encrypt_password(data["password"])
        self.conn.execute(
            query, (data["website"], data["username"], encryptedpass, data["ID"])
        )
        self.conn.commit()

    def dbDelEntry(self, id):
        query = "DELETE FROM user_accounts WHERE id = ?"
        self.conn.execute(query, (id,))
        self.conn.commit()

    def search_entry(self, search_term):
        query = """
            SELECT * FROM user_accounts
            WHERE website LIKE ? """
        self.cur.execute(query, (f"%{search_term}%",))
        return self.cur.fetchall()
