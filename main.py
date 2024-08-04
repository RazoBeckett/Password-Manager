# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2024 @razobeckett

import os
import re
import sqlite3
import tkinter as tk
from tkinter import messagebox

import bcrypt

from password_manager import MainPage


# Function to hash the master password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


# Function to check if the database file exists
def check_database():
    if not os.path.exists("passwords.db"):
        create_database()


# Function to create the database file and the passwords table if it doesn't exist
def create_database():
    conn = sqlite3.connect("passwords.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS passwords
                 (website TEXT, username TEXT, password TEXT)"""
    )
    conn.commit()
    conn.close()


def set_master_password():
    master_password = master_password_entry.get()
    confirm_password = confirm_password_entry.get()
    if master_password and confirm_password:
        if master_password == confirm_password:

            def is_strong(x):
                return all(
                    [
                        len(x) >= 8,
                        re.search(r"[a-z]", x),
                        re.search(r"[A-Z]", x),
                        re.search(r"[0-9]", x),
                        re.search(r"[!@#$%^&*()_+]", x),
                    ]
                )

            if not is_strong(master_password):
                messagebox.showerror(
                    "Error",
                    "Password should contain at least 8 characters, one digit, one upper case, one lower case and one special character.",
                )
                return

            create_database()  # Ensure the database and table are created
            hashed_password = hash_password(master_password)
            conn = sqlite3.connect("passwords.db")
            c = conn.cursor()
            # Check if the table exists, if not, create it
            c.execute(
                """CREATE TABLE IF NOT EXISTS master_password (hashed_password TEXT)"""
            )
            c.execute(
                "INSERT INTO master_password (hashed_password) VALUES (?)",
                (hashed_password,),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Master password set successfully.")
            login_window.destroy()
        else:
            messagebox.showerror("Error", "Passwords do not match. Please try again.")
    else:
        messagebox.showerror("Error", "Please enter a password.")


# Function to check if the entered password is correct
def check_password(master_password):
    conn = sqlite3.connect("passwords.db")
    c = conn.cursor()
    try:
        c.execute("SELECT hashed_password FROM master_password")
        stored_hashed_password = c.fetchone()[0]

        if bcrypt.checkpw(master_password.encode(), stored_hashed_password):
            try:
                MainPage(master_password)
            except Exception:
                messagebox.showerror(
                    "Error",
                    "Failed to open password manager, please check if password_manager.py is in the same directory.",
                )
        else:
            messagebox.showerror("Error", "Incorrect password. Access denied.")
    except:
        messagebox.showerror("Error", "Master password is not set.")
    finally:
        conn.close()


# Create the main Tkinter window
root = tk.Tk()
root.title("Password Manager")
root.geometry("400x200")
root.resizable(False, False)

# Check if the database exists
check_database()


# Function to handle the login button click
def login():
    master_password = password_entry.get()
    if master_password:
        check_password(master_password)
    else:
        messagebox.showerror("Error", "Please enter a password.")


# Function to handle the set password button click
def set_password():
    global login_window
    login_window = tk.Toplevel(root)
    login_window.title("Set Master Password")

    master_password_label = tk.Label(login_window, text="Enter Master Password:")
    master_password_label.pack()
    global master_password_entry
    master_password_entry = tk.Entry(login_window, show="*")
    master_password_entry.pack()

    confirm_password_label = tk.Label(login_window, text="Confirm Master Password:")
    confirm_password_label.pack()
    global confirm_password_entry
    confirm_password_entry = tk.Entry(login_window, show="*")
    confirm_password_entry.pack()

    os.remove("passwords.db")
    set_password_button = tk.Button(
        login_window, text="Set Password", command=set_master_password
    )
    set_password_button.pack()


# Create and pack GUI elements
password_label = tk.Label(root, text="Enter Master Password:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()
login_button = tk.Button(root, text="Login", command=login)
login_button.pack()

set_password_button = tk.Button(root, text="Set Master Password", command=set_password)
set_password_button.pack()

# Run the Tkinter event loop
root.mainloop()
root.quit()
