import tkinter as tk
from tkinter import END, messagebox, ttk

from db_operations import dbOperation
from PasswordGenerator import PasswordGenerator


class MainPage:
    def __init__(self, master_password):
        self.db = dbOperation(master_password)
        self.root = tk.Tk()
        headTitle = tk.Label(
            self.root,
            text="Python Password Manager",
            font=("Arial", 24),
            justify="center",
        )
        headTitle.grid(
            columnspan=4, padx=140, pady=10
        )  # Use grid() instead of pack() for better control
        self.root.title("Python Password Manager")
        self.root.geometry("1000x600+40+40")
        self.root.resizable(False, False)

        self.curd_frame = tk.Frame(
            self.root,
            highlightbackground="black",
            highlightthickness=1,
            padx=10,
            pady=10,
        )
        self.curd_frame.grid()
        self.EntryLabels()
        self.EntryFields()
        self.Buttons()
        self.search_Entry = tk.Entry(self.curd_frame, width=30, font=("Arial", 12))
        self.search_Entry.grid(row=self.rowno, column=self.colno)
        tk.Button(
            self.curd_frame,
            text="Search",
            bg="black",
            fg="white",
            font=("Arial", 12),
            width=20,
            command=self.search_entry,
        ).grid(row=self.rowno, column=self.colno + 1, padx=10, pady=5)
        self.entrytree()
        self.root.mainloop()

    def EntryLabels(self):
        self.colno, self.rowno = 0, 0
        labelsInfo = ("ID", "Website", "Username", "Password")
        for labelName in labelsInfo:
            tk.Label(
                self.curd_frame, text=labelName, font=("Arial", 12), bg="grey"
            ).grid(row=self.rowno, column=self.colno, padx=10, pady=5)
            self.colno += 1

    def Buttons(self):
        self.rowno += 1
        self.colno = 0
        Buttonss = (
            ("Save", "green", self.saveEntry),
            ("Update", "blue", self.updateEntry),
            ("Delete", "red", self.delEntry),
            ("Copy Password", "violet", self.copy2clip),
            ("Show All", "black", self.showAllEntry),
            (
                "Generate Pass",
                "orange",
                self.openPasswordGenerator,
            ),
        )
        for bInfo in Buttonss:
            if bInfo[0] == "Show All":
                self.rowno += 1
                self.colno = 0
            tk.Button(
                self.curd_frame,
                text=bInfo[0],
                bg=bInfo[1],
                fg="white",
                font=("Arial", 12),
                padx=5,
                pady=2,
                width=12,
                command=bInfo[2],
            ).grid(row=self.rowno, column=self.colno, padx=2, pady=10)
            self.colno += 1

    def EntryFields(self):
        self.rowno, self.colno = 1, 0
        self.entrybox = []
        for i in range(4):
            show = ""
            if i == 3:
                show = "*"
            entrybox = tk.Entry(
                self.curd_frame,
                width=22,
                font=("Arial", 12),
                show=show,
            )
            entrybox.grid(row=self.rowno, column=self.colno, padx=10, pady=5)
            if i == 0:
                entrybox.bind("<Key>", lambda e: "break")
            self.colno += 1
            self.entrybox.append(entrybox)

    def saveEntry(self):
        website = self.entrybox[1].get()
        username = self.entrybox[2].get()
        password = self.entrybox[3].get()
        data = {"website": website, "username": username, "password": password}
        print(data)
        self.db.dbSaveEntry(data)
        self.showAllEntry()

    def updateEntry(self):
        id = self.entrybox[0].get()
        website = self.entrybox[1].get()
        username = self.entrybox[2].get()
        password = self.entrybox[3].get()
        data = {
            "ID": id,
            "website": website,
            "username": username,
            "password": password,
        }
        self.db.dbUpdateEntry(data)
        self.showAllEntry()

    def delEntry(self):
        id = self.entrybox[0].get()
        self.db.dbDelEntry(id)
        self.showAllEntry()
        for entry_box in self.entrybox:
            entry_box.delete(0, END)

    def showAllEntry(self):
        for item in self.EntryTree.get_children():
            self.EntryTree.delete(item)
        entryList = self.db.dbGetAllEntry()
        for entry in entryList:
            self.EntryTree.insert(
                "", END, values=(entry[0], entry[1], entry[2], entry[3])
            )

    def entrytree(self):
        col = ("ID", "Website", "Username", "Password")
        self.EntryTree = ttk.Treeview(self.root, columns=col, show="headings")
        self.EntryTree.heading("ID", text="ID")
        self.EntryTree.heading("Website", text="Website Name")
        self.EntryTree.heading("Username", text="Username")
        self.EntryTree.heading("Password", text="Password")
        self.EntryTree["displaycolumns"] = ("ID", "Website", "Username", "Password")

        def item_selected(event):
            for selected_item in self.EntryTree.selection():
                item = self.EntryTree.item(selected_item)
                entry = item["values"]
                for entry_box, item in zip(self.entrybox, entry):
                    entry_box.delete(0, END)
                    entry_box.insert(0, item)

        self.EntryTree.bind("<<TreeviewSelect>>", item_selected)
        self.EntryTree.grid()

    def copy2clip(self):
        if self.entrybox[3].get() == "":
            message = "No Password to Copy"
            title = "No Password"
            messagebox.showinfo(title, message, icon="warning")
        else:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.entrybox[3].get())
            message = "Password Copied to Clipboard"
            title = "Password Copied"
            messagebox.showinfo(title, message, icon="info")

    def openPasswordGenerator(self):
        PasswordGenerator(tk.Toplevel(self.root))

    def search_entry(self):
        search_term = self.search_Entry.get()
        if not search_term:
            messagebox.showwarning("Search Error", "Please enter a search term.")
            return
        result = self.db.search_entry(search_term)
        if result:
            self.showAllEntry()
        else:
            messagebox.showinfo("Search Result", "No matching entry found.")


if __name__ == "__main__":
    dbClass = dbOperation()
    root = tk.Tk()
    MainPage(root, dbClass)
    root.mainloop()
