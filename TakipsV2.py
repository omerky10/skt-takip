
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import datetime
import telegram

class Product:
    def __init__(self, name, start_date, end_date):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.products = []
        self.check_expiration()

    def create_widgets(self):
        self.product_name_label = tk.Label(self, text="Product Name")
        self.product_name_label.pack()
        
        self.product_name = tk.StringVar()
        self.product_name_entry = tk.Entry(self, textvariable=self.product_name)
        self.product_name_entry.pack()
        
        self.start_date_label = tk.Label(self, text="Start Date (YYYY-MM-DD)")
        self.start_date_label.pack()
        
        self.start_date = tk.StringVar()
        self.start_date_entry = tk.Entry(self, textvariable=self.start_date)
        self.start_date_entry.pack()
        
        self.end_date_label = tk.Label(self, text="End Date (YYYY-MM-DD)")
        self.end_date_label.pack()
        
        self.end_date = tk.StringVar()
        self.end_date_entry = tk.Entry(self, textvariable=self.end_date)
        self.end_date_entry.pack()
        
        self.add_product_button = tk.Button(self, text="ADD", command=self.add_product)
        self.add_product_button.pack()
        
        self.tree = ttk.Treeview(self, columns=("Start Date", "End Date", "Status"))
        self.tree.heading("#0", text="Product Name")
        self.tree.heading("Start Date", text="Start Date")
        self.tree.heading("End Date", text="End Date")
        self.tree.heading("Status", text="Status")
        self.tree.column("#0", stretch=tk.YES)
        self.tree.column("Start Date", stretch=tk.YES)
        self.tree.column("End Date", stretch=tk.YES)
        self.tree.column("Status", stretch=tk.YES)
        self.tree.pack()
        self.delete_product_button = tk.Button(self, text="DELETE", command=self.delete_product)
        self.delete_product_button.pack()
        self.edit_product_button = tk.Button(self, text="EDIT", command=self.edit_product)
        self.edit_product_button.pack()

    def add_product(self):
        name = self.product_name.get()
        start = self.start_date.get()
        end = self.end_date.get()
        try:
            datetime.datetime.strptime(start, '%Y-%m-%d')
            datetime.datetime.strptime(end, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Incorrect date format. Use YYYY-MM-DD")
            return
        if not name or not start or not end:
            messagebox.showerror("Error", "All fields are required")
            return
        self.products.append(Product(name, start, end))
        self.tree.insert("", "end", text=name, values=(start, end, "Not expired"))
        self.product_name.set("")
        self.start_date.set("")
        self.end_date.set("")
    def delete_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No product selected")
            return
        name = self.tree.item(selected_item)["text"]
        for product in self.products:
            if product.name == name:
                self.products.remove(product)
                break
        self.tree.delete(selected_item)
    def edit_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No product selected")
            return
        name = self.tree.item(selected_item)["text"]
        for product in self.products:
            if product.name == name:
                self.product_name.set(product.name)
                self.start_date.set(product.start_date)
                self.end_date.set(product.end_date)
                self.products.remove(product)
                self.tree.delete(selected_item)
                break

    def send_message(message):
        bot = telegram.Bot(token='6289548429:AAFcVzfljxgtHZR7DDlEjo4fDNlVPB4qMp4')
        chat_id = '-1001814445707'  
        bot.send_message(chat_id=chat_id, text=message)

    def check_expiration(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        for product in self.products:
            if now >= product.end_date:
                self.tree.insert("", "end", text=product.name, values=(product.start_date, product.end_date, "Expired"))
                send_message(f"{product.name} has expired on {product.end_date}")
            else:
                self.tree.insert("", "end", text=product.name, values=(product.start_date, product.end_date, "Not expired"))

root = tk.Tk()
app = Application(master=root)
app.mainloop()
