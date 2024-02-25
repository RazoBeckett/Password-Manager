import tkinter as tk

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Password Manager")

        # Username label and entry
        self.username_label = tk.Label(root, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.username_entry = tk.Entry(root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        # Password label and entry
        self.password_label = tk.Label(root, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Login button
        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.grid(row=2, column=1, padx=10, pady=5)

    def login(self):
        # Retrieve username and password from entry fields
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Replace this with your authentication logic
        print(f"Username: {username}, Password: {password}")

if __name__ == "__main__":
    root = tk.Tk()
    LoginPage(root)
    root.mainloop()
