# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 @razobeckett

import os
import sqlite3

import bcrypt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def pad(data):
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    return padded_data


def unpad(data):
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(data) + unpadder.finalize()
    return unpadded_data


def generate_key(password):
    key = bcrypt.kdf(
        password=password.encode(), salt=b"salt", desired_key_bytes=32, rounds=100
    )
    return key


def encrypt_password(password, key):
    backend = default_backend()
    iv = os.urandom(16)  # Generate a random initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(pad(password.encode())) + encryptor.finalize()
    return iv + ciphertext


def decrypt_password(encrypted_password, key):
    backend = default_backend()
    iv = encrypted_password[:16]
    ciphertext = encrypted_password[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return unpad(plaintext)


class dbOperation:
    def __init__(self, masterpassword):
        self.db_file = "passwords.db"
        self.conn = self.connect()
        self.cur = self.conn.cursor()
        self.create_table()
        self.key = generate_key(masterpassword)

    def connect(self):
        return sqlite3.connect(self.db_file)

    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS user_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website TEXT NOT NULL,
                username TEXT NOT NULL,
                password BLOB NOT NULL
            )
        """
        self.conn.execute(query)
        self.conn.commit()

    def dbSaveEntry(self, data):
        # Get the maximum ID in the database
        max_id_query = "SELECT MAX(id) FROM user_accounts"
        max_id_result = self.conn.execute(max_id_query).fetchone()
        max_id = max_id_result[0] if max_id_result[0] is not None else 0

        # Insert the new entry with an ID one greater than the maximum ID
        query = """INSERT INTO user_accounts (id, website, username, password) VALUES (?, ?, ?, ?)"""
        encryptedpass = encrypt_password(data["password"], self.key)
        self.conn.execute(
            query, (max_id + 1, data["website"], data["username"], encryptedpass)
        )
        self.conn.commit()

    def dbGetAllEntry(self):
        query = "SELECT * FROM user_accounts"
        entries = self.conn.execute(query).fetchall()
        decrypted_entries = []
        for entry in entries:
            decrypted_entry = list(entry)
            encrypted_password = entry[3]
            decrypted_entry[3] = decrypt_password(encrypted_password, self.key).decode()
            decrypted_entries.append(tuple(decrypted_entry))
        return decrypted_entries

    def dbUpdateEntry(self, data):
        query = "UPDATE user_accounts SET website = ?, username = ?, password = ? WHERE id = ?"
        encryptedpass = encrypt_password(data["password"], self.key)
        self.conn.execute(
            query, (data["website"], data["username"], encryptedpass, data["ID"])
        )
        self.conn.commit()

    def dbDelEntry(self, id):
        # Delete the entry with the given ID
        query_delete = "DELETE FROM user_accounts WHERE id = ?"
        self.conn.execute(query_delete, (id,))

        # After deleting, update the IDs to be sequential
        query_update = "UPDATE user_accounts SET id = id - 1 WHERE id > ?"
        self.conn.execute(query_update, (id,))

        # Commit both operations
        self.conn.commit()

    def search_entry(self, search_term):
        query = """SELECT ID, website FROM user_accounts WHERE website LIKE ?"""
        self.cur.execute(query, (f"%{search_term}%",))
        result = self.cur.fetchall()
        if result:
            return result[0]
        else:
            return None

    def entryExists(self, website, username):
        query = "SELECT * FROM user_accounts WHERE website = ? AND username = ?"
        self.cur.execute(query, (website, username))
        result = self.cur.fetchall()
        return len(result) > 0
