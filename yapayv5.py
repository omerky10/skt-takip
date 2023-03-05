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
from telebot.types import Message
tracemalloc.start()


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

        self.Bot_run = tk.Button(self, text="Botu Çalıştır", command=self.Take)
        self.Bot_run.pack(side=tk.LEFT, padx=5)

        self.file_path = "products.pickle"  # dosya yolunu belirleyin
        try:
            with open(self.file_path, "rb") as f:
                self.products = pickle.load(f)
        except FileNotFoundError:
            self.products = []

        self.load_products()

    def Take(self):
        self.botTake = telebot.TeleBot(
            "6289548429:AAFcVzfljxgtHZR7DDlEjo4fDNlVPB4qMp4")

        # Tarih formatı
        self.DATE_FORMAT = "%d/%m/%Y"

        # Mesajları işlemeyi sürdürmek için bir bayrak
        self.processing_messages = False

        # Gelen mesajları işleyin

        @self.botTake.message_handler(commands=['skt'])
        def start_processing_messages(message):
            global processing_messages
            processing_messages = True
            self.botTake.reply_to(
                message, "Hoşgeldin . Mesajları kaydetmeye başladım.")

        @self.botTake.message_handler(commands=['quit'])
        def stop_processing_messages(message):
            global processing_messages
            processing_messages = False
            self.botTake.reply_to(message, "Mesajları kaydetmeyi bıraktım.")
            self.botTake.stop_polling()

        @self.botTake.message_handler(func=lambda message: processing_messages)
        def handle_message(message):
            # Mesajı ayrıştır
            message_parts = message.text.split()
            if len(message_parts) != 2:
                self.botTake.reply_to(
                    message, "Hatalı mesaj formatı! Lütfen mesajda ürün adı ve son kullanma tarihini bir boşlukla ayırın.")
                return
            name, expiration_date = message_parts
            # Tarih formatını kontrol et
            try:
                expiration_date = datetime.strptime(
                    expiration_date, self.DATE_FORMAT).date()
                expiration_date = expiration_date.strftime('%d/%m/%Y')
            except ValueError:
                self.botTake.reply_to(
                    message, "Hatalı tarih formatı! Lütfen tarihi dd/mm/yyyy formatında girin.")
                return

            # pickle dosyasını yükle veya boş bir liste oluştur
            try:
                with open(self.file_path, 'rb') as f:
                    messages = pickle.load(f)
            except EOFError:
                messages = []

            # Name kontrolü yap ve tarih kontrolü yap
            updated = False
            for message in messages:
                if message['name'] == name:
                    # SKT bilgisini kontrol et ve gerekirse güncelle
                    if message.get('expiration_date') is not None and message.get('expiration_date') != 'SKT Girdi':
                        try:
                            expiration_date_string = str(
                                message['expiration_date'])
                            expiration_date_in_file = datetime.strptime(
                                expiration_date_string, self.DATE_FORMAT).date()
                            if (expiration_date_in_file - datetime.now().date()).days < 0:
                                message['status'] = 'SKT girdi'
                            else:
                                message['status'] = 'SKT Bekleniyor'
                        except ValueError:
                            pass
                    # Tarihi güncelle
                    message['expiration_date'] = expiration_date
                    updated = True

            # Eğer güncelleme yapıldıysa, verileri dosyaya kaydet
            if updated:
                with open(self.file_path, "wb") as f:
                    pickle.dump(messages, f)
            else:
                # Yeni mesajı ekle
                message_dict = {
                    "name": name, "expiration_date": expiration_date}
                messages.append(message_dict)
                # Mesajı ekrana yazdır
                print(message_dict)
                with open(self.file_path, "wb") as f:
                    pickle.dump(messages, f)

        # Botu çalıştırın
        self.botTake.polling()

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
            # load products from file
            with open("products.pickle", "rb") as f:
                existing_products = pickle.load(f)

            # check if the selected product already exists
            for product in existing_products:
                if product["name"] == name:
                    tk.messagebox.showerror(
                        "Hata", "Bu ürün zaten kaydedilmiş!")
            self.products.append(selected_item_data)
            self.load_products()
            self.save_products()
            self.name_entry.delete(0, tk.END)
            self.expiration_entry.delete(0, tk.END)
        except ValueError:
            tk.messagebox.showerror(
                "Hata", "Lütfen geçerli bir SKT girin (gg/aa/yyyy) veya bu ürün listenizde mevcud.")

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


if __name__ == "__main__":
    app = App()
    app.mainloop()
