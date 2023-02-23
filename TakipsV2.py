import tkinter as tk
import tkinter.ttk as ttk
import time
import telegram
import cv2
import pytesseract
import sqlite3
import pandas as pd


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Set Takip Sistemi")
        self.geometry("500x500")

        self.tree = ttk.Treeview(self, columns=(
            "start_date", "end_date", "status"))
        self.tree.heading("#0", text="Ürün İsmi")
        self.tree.heading("start_date", text="Başlangıç Tarihi")
        self.tree.heading("end_date", text="Bitiş Tarihi")
        self.tree.heading("status", text="Durum")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.name_entry = tk.Entry(self, width=20)
        self.add_entry = tk.Entry(self, width=20)
        self.end_entry = tk.Entry(self, width=20)

        datepicker = ttk.Button(self, text="Tarih Seç",
                                command=self.select_date)
        datepicker.pack()

        add_button = ttk.Button(self, text="Ekle", command=self.add_product)
        add_button.pack()

        delete_button = ttk.Button(
            self, text="Sil", command=self.delete_product)
        delete_button.pack()

        edit_button = ttk.Button(self, text="Düzenle",
                                 command=self.edit_product)
        edit_button.pack()

        self.products = []
        self.timer = None

        self.telegram_bot = telegram.Bot(
            token="6289548429:AAFcVzfljxgtHZR7DDlEjo4fDNlVPB4qMp4")
        self.telegram_chat_id = "-1001814445707"

        self.conn = sqlite3.connect("products.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            start_date TEXT,
            end_date TEXT,
            status TEXT
        )
        """)
        self.conn.commit()

        self.load_data()

    def select_date(self):
        pass  # datepicker implementation

    def add_product(self):
        name = self.name_entry.get()
        start_date = self.start_entry.get()
        end_date = self.end_entry.get()

        self.cursor.execute(
            "INSERT INTO products (name, start_date, end_date) VALUES (?, ?, ?)", (name, start_date, end_date))
        self.conn.commit()

        self.tree.insert("", "end", text=name, values=(
            start_date, end_date, "Active"))
        self.start_timer(end_date, name)

    def delete_product(self):
        selected = self.tree.selection()
        for item in selected:
            self.tree.delete(item)
            name = self.tree.item(item, "text")
            self.cursor.execute("DELETE FROM products WHERE name=?", (name,))
            self.conn.commit()

            for product in self.products:
                if product["name"] == name:
                    self.products.remove(product)
                    break

            if self.timer:
                self.after_cancel(self.timer)

    def edit_product(self):
        selected_item = self.tree.selection()[0]
        name = self.name_entry.get()
        start_date = self.start_entry.get()
        end_date = self.end_entry.get()

        self.cursor.execute("UPDATE products SET name=?, start_date=?, end_date=? WHERE name=?",
                            (name, start_date, end_date, self.tree.item(selected_item, "text")))
        self.conn.commit()

        self.tree.item(selected_item, text=name, values=(
            start_date, end_date, "Active"))
        self.start_timer(end_date, name)

    def load_data(self):
        data = pd.read_sql_query("SELECT * FROM products", self.conn)
        for index, row in data.iterrows():
            self.products.append(
                {"name": row["name"], "start": row["start_date"], "end": row["end_date"]})
            self.tree.insert("", "end", text=row["name"], values=(
                row["start_date"], row["end_date"], row["status"]))
            self.start_timer(row["end_date"], row["name"])

    def start_timer(self, end_date, name):
        now = time.time()
        end_time = time.mktime(time.strptime(end_date, "%d.%m.%Y"))

        if end_time > now:
            self.timer = self.after(
                int((end_time - now) * 1000), self.send_notification, name)

    def send_notification(self, name):
        self.telegram_bot.send_message(
            chat_id=self.telegram_chat_id, text=f"{name} SKT geçti")
        self.cursor.execute(
            "UPDATE products SET status='Expired' WHERE name=?", (name,))
        self.conn.commit()

    def refresh(self):
        self.after(10000, self.refresh)

        img = cv2.imread("<image_path>")
        text = pytesseract.image_to_string(img)
        data = text.split("\n")

        for item in data:
            item_data = item.split(" ")
            name = item_data[0]
            end_date = item_data[1]
            self.cursor.execute(
                "UPDATE products SET end_date=? WHERE name=?", (end_date, name))
            self.conn.commit()

            for product in self.products:
                if product["name"] == name:
                    product["end"] = end_date
                    self.tree.item(product, values=(
                        product["start"], product["end"], "Active"))
                    break

        self.start_timer(end_date, name)


app = Application()
app.after(0, app.refresh)
app.mainloop()
