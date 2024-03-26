import random
import string
import tkinter as tk
from tkinter import messagebox, ttk


class PasswordGenerator:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Password Generator")

        # Create and place widgets
        self.length_label = tk.Label(parent, text="Password Length:")
        self.length_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.length_slider = ttk.Scale(
            parent,
            from_=16,
            to=64,
            orient="horizontal",
            command=self.update_length_label,
        )
        self.length_slider.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Label to display selected password length
        self.length_display_label = tk.Label(parent, text="")
        self.length_display_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        self.include_numbers_var = tk.BooleanVar()
        self.include_numbers_checkbox = tk.Checkbutton(
            parent, text="Include Numbers", variable=self.include_numbers_var
        )
        self.include_numbers_checkbox.grid(
            row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w"
        )

        self.include_symbols_var = tk.BooleanVar()
        self.include_symbols_checkbox = tk.Checkbutton(
            parent, text="Include Symbols", variable=self.include_symbols_var
        )
        self.include_symbols_checkbox.grid(
            row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w"
        )

        self.generate_button = tk.Button(
            parent, text="Generate Password", command=self.generate_button_clicked
        )
        self.generate_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.password_text = tk.Text(parent, height=1, width=30, wrap="none")
        self.password_text.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.copy_button = tk.Button(
            parent, text="Copy", command=self.copy_button_clicked
        )
        self.copy_button.grid(row=4, column=1, padx=10, pady=10, sticky="e")

        self.update_length_label(16)  # Set initial length label
        self.include_numbers_var.set(True)  # Include numbers by default

    def generate_password(self, length, include_numbers, include_symbols):
        chars = string.ascii_letters
        if include_numbers:
            chars += string.digits
        if include_symbols:
            chars += string.punctuation

        password = "".join(random.choice(chars) for _ in range(length))
        return password

    def update_length_label(self, value):
        self.length_display_label.config(text=f"Length: {int(float(value))}")

    def generate_button_clicked(self):
        length = int(self.length_slider.get())
        if not length:
            length = 16  # Default length
        include_numbers = self.include_numbers_var.get()
        include_symbols = self.include_symbols_var.get()

        password = self.generate_password(length, include_numbers, include_symbols)
        self.password_text.delete(1.0, tk.END)  # Clear previous content
        self.password_text.insert(tk.END, password)

    def copy_button_clicked(self):
        password = self.password_text.get(1.0, tk.END).strip()
        if password:
            self.parent.clipboard_clear()
            self.parent.clipboard_append(password)
            self.parent.update()
            messagebox.showinfo("Password Generator", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Password Generator", "No password to copy.")
