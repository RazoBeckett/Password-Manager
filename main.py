import os
import sqlite3
import tkinter as tk
from tkinter import messagebox
from password_manager import MainPage

import bcrypt


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
    c.execute("SELECT hashed_password FROM master_password")
    stored_hashed_password = c.fetchone()[0]
    conn.close()

    if bcrypt.checkpw(master_password.encode(), stored_hashed_password):
        messagebox.showinfo(
            "Success", "Password verified. You can now access the password manager."
        )
        try:
            MainPage()
            root.destroy()
        except Exception as e:
            messagebox.showerror(
                "Error",
                "Failed to open password manager., Please check if main.py is in the same directory.",
                e
            )
        # Code to open the password manager GUI
        # Replace this with your actual code to open the password manager
    else:
        messagebox.showerror("Error", "Incorrect password. Access denied.")


# Create the main Tkinter window
root = tk.Tk()
root.title("Password Manager")

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
