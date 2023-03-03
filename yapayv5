import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmsgbox
from datetime import datetime
import pickle
import telegram
import tracemalloc
import logging
import requests
import telebot

tracemalloc.start()
bot = telebot.TeleBot("6289548429:AAFcVzfljxgtHZR7DDlEjo4fDNlVPB4qMp4")

# Mesajları kaydetmek için bir liste oluşturun
messages = []

# Tarih formatı
DATE_FORMAT = "%d/%m/%Y"

# Mesajları işlemeyi sürdürmek için bir bayrak
processing_messages = False

# Gelen mesajları işleyin


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ürün Listesi")
        self.token = "6289548429:AAFcVzfljxgtHZR7DDlEjo4fDNlVPB4qMp4"
        self.chat_id = "-1001814445707"
        self.bot = telegram.Bot(token=self.token)

        # Treeview widget
        self.tree = ttk.Treeview(self)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Columns
        self.tree["columns"] = ("name", "expiration_date", "status")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("name", anchor=tk.W, width=200)
        self.tree.column("expiration_date", anchor=tk.W, width=200)
        self.tree.column("status", anchor=tk.W, width=200)

        # Headings
        self.tree.heading("name", text="Ürün Adı")
        self.tree.heading("expiration_date", text="SKT")
        self.tree.heading("status", text="Durum")

        # Input fields
        self.name_label = tk.Label(self, text="Ürün Adı:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        self.expiration_label = tk.Label(self, text="SKT (gg/aa/yyyy):")
        self.expiration_label.pack()
        self.expiration_entry = tk.Entry(self)
        self.expiration_entry.pack()

        # Buttons
        self.add_button = tk.Button(
            self, text="Ekle", command=self.add_product)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = tk.Button(
            self, text="Düzenle", command=self.edit_product)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(
            self, text="Sil", command=self.delete_product)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.refresh_button = tk.Button(
            self, text="Yenile", command=self.refresh_products)
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        self.file_path = "products.pickle"  # dosya yolunu belirleyin
        try:
            with open(self.file_path, "rb") as f:
                self.products = pickle.load(f)
        except FileNotFoundError:
            self.products = []

        self.load_products()

    def send_message(self, text):
        bot_token = "6289548429:AAFcVzfljxgtHZR7DDlEjo4fDNlVPB4qMp4"
        chat_id = "-1001814445707"
        send_text = 'https://api.telegram.org/bot' + bot_token + \
            '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + text
        print(send_text)
        response = requests.get(send_text)
        return response.json()

    def save_products(self):
        with open(self.file_path, "wb") as f:
            pickle.dump(self.products, f)

    def load_products(self):
        self.tree.delete(*self.tree.get_children())
        for product in self.products:
            name = product["name"]
            expiration_date_str = str(product["expiration_date"])
            status = ""
            try:
                expiration_date = datetime.strptime(
                    expiration_date_str, "%d/%m/%Y").date()
                if (expiration_date - datetime.now().date()).days < 0:
                    status = f"{name} - SKT Girdi"
                    self.send_message(f'Ürün {name} SKT Girdi')
            except ValueError:
                pass
            self.tree.insert("", tk.END, text="", values=(
                name, expiration_date_str, status))

    def add_product(self):
        name = self.name_entry.get().strip()
        expiration_date_str = self.expiration_entry.get().strip()
        try:
            expiration_date = datetime.strptime(
                expiration_date_str, "%d/%m/%Y").date()
            status = ""
            if (expiration_date - datetime.now().date()).days < 0:
                status = f"{name} - SKT Girdi"
            selected_item_data = {
                "name": name, "expiration_date": expiration_date_str, "status": status}
            self.products.append(selected_item_data)
            self.load_products()
            self.save_products()
        except ValueError:
            tk.messagebox.showerror(
                "Hata", "Lütfen geçerli bir SKT girin (gg/aa/yyyy).")

    def delete_product(self):
        selected_item = self.tree.selection()
        if len(selected_item) == 0:
            tk.messagebox.showerror("Hata", "Lütfen bir ürün seçin.")
            return

        # get the selected item's data
        selected_item_id = self.tree.index(selected_item)
        selected_item_data = self.products[selected_item_id]

        # ask for confirmation before deleting the item
        confirm = tk.messagebox.askyesno("Silmek istediğinizden emin misiniz?",
                                         f"{selected_item_data['name']} ürününü silmek istediğinizden emin misiniz?")

        if confirm:
            # delete the item from the products list
            del self.products[selected_item_id]

            # refresh the treeview
            self.load_products()
            self.save_products()  # save changes to file

    def refresh_products(self):
        # reload the products from file
        try:
            with open(self.file_path, "rb") as f:
                self.products = pickle.load(f)
        except FileNotFoundError:
            self.products = []

        self.load_products()

    def edit_product(self):
        # get the selected item
        selected_item = self.tree.selection()
        if len(selected_item) == 0:
            tk.messagebox.showerror("Hata", "Lütfen bir ürün seçin.")
            return

        # get the selected item's data
        selected_item_id = self.tree.index(selected_item)
        selected_item_data = self.products[selected_item_id]

        # open a new window to edit the item
        edit_window = tk.Toplevel(self)
        edit_window.title("Ürün Düzenle")
        edit_window.geometry("400x200")

        name_label = tk.Label(edit_window, text="Ürün Adı:")
        name_label.pack()
        name_entry = tk.Entry(edit_window)
        name_entry.pack()
        name_entry.insert(0, selected_item_data["name"])

        expiration_label = tk.Label(edit_window, text="SKT (gg/aa/yyyy):")
        expiration_label.pack()
        expiration_entry = tk.Entry(edit_window)
        expiration_entry.pack()
        expiration_entry.insert(0, selected_item_data["expiration_date"])

        # save changes button
        def save_changes():
            name = name_entry.get().strip()
            expiration_date_str = expiration_entry.get().strip()
            try:
                expiration_date = datetime.strptime(
                    expiration_date_str, "%d/%m/%Y").date()
                status = ""
                if (expiration_date - datetime.now().date()).days < 0:
                    status = f"{name} - SKT Girdi"
                selected_item_data["name"] = name
                selected_item_data["expiration_date"] = expiration_date_str
                selected_item_data["status"] = status
                self.load_products()
                self.save_products()
                edit_window.destroy()
            except ValueError:
                tk.messagebox.showerror(
                    "Hata", "Lütfen geçerli bir SKT girin (gg/aa/yyyy).")

        save_button = tk.Button(
            edit_window, text="Kaydet", command=save_changes)
        save_button.pack(pady=10)


class Take():
    bot = telebot.TeleBot("6289548429:AAFcVzfljxgtHZR7DDlEjo4fDNlVPB4qMp4")

    # Mesajları kaydetmek için bir liste oluşturun
    messages = []

    # Tarih formatı
    DATE_FORMAT = "%d/%m/%Y"

    # Mesajları işlemeyi sürdürmek için bir bayrak
    processing_messages = False

    # Gelen mesajları işleyin

    @bot.message_handler(commands=['skt'])
    def start_processing_messages(message):
        global processing_messages
        processing_messages = True
        bot.reply_to(message, "Mesajları kaydetmeye başladım.")

    @bot.message_handler(commands=['quit'])
    def stop_processing_messages(message):
        global processing_messages
        processing_messages = False
        bot.reply_to(message, "Mesajları kaydetmeyi bıraktım.")

    @bot.message_handler(func=lambda message: processing_messages)
    def handle_message(message):
        # Mesajı ayrıştır
        message_parts = message.text.split()
        if len(message_parts) != 2:
            bot.reply_to(
                message, "Hatalı mesaj formatı! Lütfen mesajda ürün adı ve son kullanma tarihini bir boşlukla ayırın.")
            return
        name, SKT = message_parts
        # Tarih formatını kontrol et
        try:
            datetime.strptime(SKT, DATE_FORMAT)
        except ValueError:
            bot.reply_to(
                message, "Hatalı tarih formatı! Lütfen tarihi dd/mm/yyyy formatında girin.")
            return
        # Yeni sözlük oluştur
        message_dict = {"name": name, "SKT": SKT}
        # Sözlüğü mesajlar listesine ekle
        messages.append(message_dict)
        # Pickle dosyasına kaydet
        with open("products.pickle", "wb") as f:
            pickle.dump(messages, f)
        # Mesajı ekrana yazdır
        print(message_dict)

    # Botu çalıştırın
    bot.polling()

if __name__ == "__main__":
    app = App()
    take = Take()
    app.mainloop()
