import tkinter as tk
from tkinter import END, ttk

from db_operations import dbOperation


class mainPage:
    def __init__(self, root, db):
        self.db = db
        self.root = root
        headTitle = tk.Label(
            self.root,
            text="Python Password Manager",
            font=("Arial", 24),
            justify="center",
        ).grid(columnspan=4, padx=140, pady=10)
        self.root.title(headTitle)
        self.root.geometry("1000x600+40+40")

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
            # command=self.searchEntry,
        ).grid(row=self.rowno, column=self.colno + 1, padx=10, pady=5)
        self.entrytree()

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
            ss = ""
            if i == 3:
                ss = "*"
            entrybox = tk.Entry(
                self.curd_frame, width=22, font=("Arial", 12), bg="lightgrey", show=ss
            )
            entrybox.grid(row=self.rowno, column=self.colno, padx=10, pady=5)
            self.colno += 1
            self.entrybox.append(entrybox)

    # curd functions
    def saveEntry(self):
        website = self.entrybox[1].get()
        username = self.entrybox[2].get()
        password = self.entrybox[3].get()
        data = {"website": website, "username": username, "password": password}
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

    def showAllEntry(self):
        for item in self.EntryTree.get_children():
            self.EntryTree.delete(item)
        entryList = self.db.dbGetAllEntry()
        for entry in entryList:
            self.EntryTree.insert(
                "", END, values=(entry[0], entry[3], entry[4], entry[5])
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

    # copy password to clipboard
    def copy2clip(self):
        if self.entrybox[3].get() == "":
            message = "No Password to Copy"
            title = "No Password"
        else:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.entrybox[3].get())
            message = "Password Copied to Clipboard"
            title = "Password Copied"
        self.showmessage(title, message)

    def showmessage(self, title_box, message):
        TIMEOUT = 1800
        popup = tk.Toplevel(self.root)
        background = "green"
        if title_box == "No Password":
            background = "red"
        popup.geometry("300x100+40+40")
        popup.title(title_box)
        label = tk.Label(popup, text=message, font=("Arial", 12), bg=background)
        label.pack(padx=10, pady=10)

        def close_popup():
            popup.destroy()

        popup.after(TIMEOUT, close_popup)


if __name__ == "__main__":
    dbClass = dbOperation()
    dbClass.createTable()
    root = tk.Tk()
    mainPage(root, dbClass)
    root.mainloop()
