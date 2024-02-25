import sqlite3


class dbOperation:
    def connect(self):
        conn = sqlite3.connect("passwords.db")
        return conn

    def createTable(self, tableName="passwords"):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS {tableName} (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            website TEXT NOT NULL, username VARCHAR(200),
            password VARCHAR(50) NOT NULL)"""
        )
        print("[DEBUG] Table created successfully")
        conn.commit()
        conn.close()

    def dbSaveEntry(self, data, tableName="passwords"):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(
            f"""INSERT INTO {tableName} ('website', 'username', 'password') VALUES (?, ?, ?)""",
            (data["website"], data["username"], data["password"]),
        )
        print("[DEBUG] Data saved successfully", data)
        conn.commit()

    def dbGetAllEntry(self, tableName="passwords"):
        conn = self.connect()
        cur = conn.cursor()
        entry = cur.execute(f"SELECT * FROM {tableName}")
        print("[DEBUG] Data fetched successfully")
        return entry

    def dbUpdateEntry(self, data, tableName="passwords"):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(
            f"""UPDATE {tableName} SET website = ?, username = ?, password = ? WHERE id = ?""",
            (data["website"], data["username"], data["password"], data["ID"]),
        )
        print("[DEBUG] Data updated successfully", data)
        conn.commit()

    def dbDelEntry(self, id, tableName="passwords"):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {tableName} WHERE id = ?", (id,))
        print("[DEBUG] Data deleted successfully")
        conn.commit()
