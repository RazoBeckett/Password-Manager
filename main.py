import tkinter as tk
from db_operations import dbOperation


class mainPage:
    def __init__(self, root, db):
        self.db = db
        self.root = root
        self.root.title("Python Password Manager")
        self.root.geometry("900x600+40+40")
        headTitle = tk.Label(
            self.root,
            text="Python Password Manager",
            font=("Arial", 24),
            justify="center",
        ).grid(columnspan=4, padx=140, pady=10)

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
        )
        for bInfo in Buttonss:
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

    def updateEntry(self):
        pass

    def delEntry(self):
        pass

    def showEntry(self):
        entryList = self.db.dbGetEntry()
        for entry in entryList:
            print(entry)

    # copy password to clipboard
    def copy2clip(self):
        pass


if __name__ == "__main__":
    dbClass = dbOperation()
    dbClass.createTable()
    root = tk.Tk()
    mainPage(root, dbClass)
    root.mainloop()
