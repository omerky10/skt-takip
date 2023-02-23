
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import telegram
import time


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Product Tracker")
        self.geometry("400x400")

        self.products = []

        self.product_name = tk.StringVar()
        self.start_date = tk.StringVar()
        self.end_date = tk.StringVar()

        self.create_widgets()
        self.tree = ttk.Treeview(self, columns=("start", "end", "status"))
        self.tree.heading("#0", text="Product Name")
        self.tree.heading("start", text="Start Date")
        self.tree.heading("end", text="End Date")
        self.tree.heading("status", text="Status")
        self.tree.column("status", width=100)
        self.tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def create_widgets(self):
        name_label = tk.Label(self, text="Product Name")
        name_label.grid(row=0, column=0, padx=10, pady=10)

        name_entry = tk.Entry(self, textvariable=self.product_name)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        start_label = tk.Label(self, text="Start Date")
        start_label.grid(row=1, column=0, padx=10, pady=10)

        start_entry = tk.Entry(self, textvariable=self.start_date)
        start_entry.grid(row=1, column=1, padx=10, pady=10)

        end_label = tk.Label(self, text="End Date")
        end_label.grid(row=2, column=0, padx=10, pady=10)

        end_entry = tk.Entry(self, textvariable=self.end_date)
        end_entry.grid(row=2, column=1, padx=10, pady=10)

        add_button = tk.Button(self, text="Add", command=self.add_product)
        add_button.grid(row=3, column=0, padx=10, pady=10)

        delete_button = tk.Button(
            self, text="Delete", command=self.delete_product)
        delete_button.grid(row=3, column=1, padx=10, pady=10)

        self.tree = ttk.Treeview(self, columns=("start", "end"))
        self.tree.heading("#0", text="Product Name")
        self.tree.heading("start", text="Start Date")
        self.tree.heading("end", text="End Date")
        self.tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def add_product(self):
        name = self.product_name.get()
        start = self.start_date.get()
        end = self.end_date.get()
        self.tree.insert("", "end", text=name, values=(start, end, ""))

        if not name or not start or not end:
            messagebox.showerror("Error", "All fields are required")
            return

        self.products.append({
            "name": name,
            "start": start,
            "end": end
        })

        self.tree.insert("", "end", text=name, values=(start, end))

        self.product_name.set("")
        self.start_date.set("")
        self.end_date.set("")

    def delete_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected")
            return

        name = self.tree.item(selected_item)["text"]
        self.tree.delete(selected_item)

        for product in self.products:
            if product["name"] == name:
                self.products.remove(product)
                break

    def check_expiry(self):
        current_time = time.strftime("%d.%m.%Y")
        for i, product in enumerate(self.products):
            if product["end"] < current_time:
                self.tree.item(self.tree.get_children()[i], values=(
                    "", "", "Tarihi Geçti"), tags=("expired",))
                self.tree.tag_configure("expired", background="red")
        bot = telegram.Bot(
            token="6289548429:AAFcVzfljxgtHZR7DDlEjo4fDNlVPB4qMp4")
        for product in self.products:
            if product["end"] < current_time:
                bot.send_message(chat_id="1001814445707",
                                 text=f"{product['name']} SKT geçti")


if __name__ == "__main__":
    app = Application()
    app.after(1000, app.check_expiry)
    app.mainloop()
