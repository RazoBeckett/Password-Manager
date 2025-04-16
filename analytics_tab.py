# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 @razobeckett

import re
import tkinter as tk
from collections import Counter
from tkinter import ttk

import matplotlib.pyplot as plt
import pwnedpasswords
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AnalyticsTab:
    def __init__(self, parent_frame, db):
        self.db = db
        self.frame = parent_frame
        self.password_data = []
        self.scores = []
        self.strength_labels = []
        self.selected_passwords = {}
        self.tree = None
        self.chart_frame = None

        self.setup_ui()

    def setup_ui(self):
        # Split vertically into top and bottom
        top_frame = tk.Frame(self.frame)
        top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        bottom_frame = tk.Frame(self.frame)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # ---- LEFT AREA (Leak Info + Donut Chart) ----
        left_analytics_frame = tk.Frame(top_frame, bg="#1E172F", width=300)
        left_analytics_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(20, 10), pady=20)

        self.leak_display_frame = tk.Frame(left_analytics_frame, bg="#1E172F")
        self.leak_display_frame.pack(pady=(10, 30))

        self.leak_status_label = tk.Label(
            self.leak_display_frame,
            text="Leaked",
            font=("Segoe UI", 28, "bold"),
            fg="#FF4C4C",
            bg="#1E172F",
        )
        self.leak_status_label.pack()

        self.leak_count_label = tk.Label(
            self.leak_display_frame,
            text="0 Times",
            font=("Segoe UI", 14),
            fg="white",
            bg="#1E172F",
        )
        self.leak_count_label.pack()

        # Donut chart frame
        self.chart_frame = tk.Frame(left_analytics_frame, bg="#1E172F")
        self.chart_frame.pack(pady=(10, 0), fill=tk.BOTH, expand=True)

        # ---- RIGHT AREA (Table) ----
        self.table_frame = tk.Frame(top_frame)
        self.table_frame.pack(
            side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 20), pady=20
        )

        self.tree = None
        self.create_table()

        # Initial data load
        self.refresh()

    def refresh(self):
        self.password_data = self.db.dbGetAllEntry()
        self.analyze_passwords()
        self.update_table()
        self.update_chart()

    def analyze_passwords(self):
        self.strength_labels.clear()
        self.scores.clear()

        for entry in self.password_data:
            password = entry[3]
            score = self.calculate_strength(password)
            self.scores.append(score)
            if score <= 2:
                self.strength_labels.append("Weak")
            elif score <= 4:
                self.strength_labels.append("Moderate")
            else:
                self.strength_labels.append("Strong")

    def calculate_strength(self, password):
        score = 0
        if len(password) >= 8:
            score += 1
        if re.search(r"[A-Z]", password):
            score += 1
        if re.search(r"[a-z]", password):
            score += 1
        if re.search(r"[0-9]", password):
            score += 1
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            score += 1
        return score

    def create_table(self):
        tree_frame = tk.Frame(self.table_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("Website", "Username", "Strength")
        self.tree = ttk.Treeview(
            tree_frame, columns=columns, show="headings", height=10
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=150)

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.check_selected_password_leak)

        # ---- Password Reuse Table ----
        self.reuse_label = tk.Label(
            self.table_frame, text="Password Reuse Found", font=("Segoe UI", 12, "bold")
        )
        self.reuse_label.pack(pady=(10, 0))
        self.reuse_label.pack_forget()  # Hide by default

        self.reuse_tree = ttk.Treeview(
            self.table_frame, columns=("Website", "Username"), show="headings", height=5
        )
        self.reuse_tree.heading("Website", text="Website")
        self.reuse_tree.heading("Username", text="Username")
        self.reuse_tree.column("Website", anchor=tk.CENTER, width=150)
        self.reuse_tree.column("Username", anchor=tk.CENTER, width=150)
        self.reuse_tree.pack(pady=(0, 20), fill=tk.X)
        self.reuse_tree.pack_forget()  # Hide by default

    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.selected_passwords.clear()

        for i, (entry, strength) in enumerate(
            zip(self.password_data, self.strength_labels)
        ):
            website, username, password = entry[1], entry[2], "*" * len(entry[3])
            item_id = self.tree.insert("", tk.END, values=(website, username, strength))
            self.selected_passwords[item_id] = entry[3]

    def update_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        counts = Counter(self.strength_labels)
        labels = list(counts.keys())
        sizes = list(counts.values())
        colors = ["#FF6B6B", "#FFD93D", "#6BCB77"]

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.set_facecolor("none")
        ax.pie(
            sizes,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
            colors=colors,
            wedgeprops={"width": 0.4},
        )
        ax.axis("equal")

        chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack()

    def check_selected_password_leak(self, _event=None):
        selected_item = self.tree.focus()
        if not selected_item:
            return

        password = self.selected_passwords.get(selected_item)
        if not password:
            return

        try:
            count = pwnedpasswords.check(password)
        except Exception:
            self.leak_status_label.config(text="Error", fg="orange")
            self.leak_count_label.config(text="Check Failed")
            return

        if count:
            self.leak_status_label.config(text="Leaked", fg="#FF4C4C")
            self.leak_count_label.config(text=f"{count:,} Times")
        else:
            self.leak_status_label.config(text="Safe", fg="#6BCB77")
            self.leak_count_label.config(text="Not Found")

        # --- Password Reuse Check ---
        reuse_records = [entry for entry in self.password_data if entry[3] == password]

        # If more than one use found (i.e. reused), exclude the currently selected record
        if len(reuse_records) > 1:
            # Clear and repopulate reuse table
            for row in self.reuse_tree.get_children():
                self.reuse_tree.delete(row)

            # Find the selected record
            selected_values = self.tree.item(selected_item)["values"]
            selected_website = selected_values[0]
            selected_username = selected_values[1]

            selected_entry = next(
                (entry for entry in reuse_records if entry[1] == selected_website and entry[2] == selected_username),
                None
            )


            filtered_records = [entry for entry in reuse_records if entry != selected_entry]

            if filtered_records:
                self.reuse_label.pack()
                self.reuse_tree.pack()
                for entry in filtered_records:
                    self.reuse_tree.insert("", tk.END, values=(entry[1], entry[2]))
            else:
                self.reuse_tree.pack_forget()
                self.reuse_label.pack_forget()
        else:
            self.reuse_tree.pack_forget()
            self.reuse_label.pack_forget()
