import json
import os
from datetime import datetime
from module.transaction import Transaction
from module.Manager.TransactionManager import TransactionManager

class ItemsManager : 
    """
    Mengelola data item dalam file JSON.

    Fitur:
    - Tambah item baru
    - Hapus item berdasarkan ID/nama
    - Edit item (misalnya stok atau harga)
    - Cari item
    - Load dan simpan data ke file JSON
    - dll
    """
    def __init__(self):    
        self.data = {"categories": {}, "items": {}}
        self.load_data()

    def load_data(self):
        if not os.path.exists('data/items.json'):
            print("File items.json tidak ditemukan, membuat file baru dengan data default.")
            self.save_data()  
        else:
            try:
                with open('data/items.json', 'r') as f:
                    content = f.read()
                    if not content:  
                        print("File items.json kosong, menulis data default.")
                        self.save_data()  
                    else:
                        self.data = json.loads(content)
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error saat memuat data: {e}")
                raise e

    def save_data(self):
        # Pastikan direktori data ada
        os.makedirs('data', exist_ok=True)
        with open('data/items.json', 'w') as f:
            json.dump(self.data, f, indent=4)

    # CRUD untuk Categories
    def get_all_categories(self):
        categories = self.data.get("categories", {})
        return categories

    def add_category(self, category_name):
        category_id = str(len(self.data["categories"]) + 1)
        self.data["categories"][category_id] = category_name
        self.save_data()

    def edit_category(self, category_id, new_name):
        if category_id in self.data["categories"]:
            self.data["categories"][category_id] = new_name
            self.save_data()

    def delete_category(self, category_id):
        if category_id in self.data["categories"]:
            del self.data["categories"][category_id]
            self.save_data()

    # CRUD untuk Items
    def get_all_items(self):
        return self.data.get("items", {})

    def get_item(self, item_name):
        return self.data["items"].get(item_name)

    def add_item(self, item_name, item_data):
        self.data["items"][item_name] = item_data
        self.save_data()

    def update_item(self, item_name, item_data):
        items = self.data["items"]
        
        # Hapus key lama jika nama diubah
        new_name = item_data["name"]
        if item_name != new_name:
            if new_name in items:
                print("Item dengan nama baru sudah ada!")  # bisa ganti jadi error handling
                return
            del items[item_name]
        
        # Simpan dengan key baru (tetap old_name kalau tidak berubah)
        items[new_name] = item_data
        self.save_data()

    def delete_item(self, item_name):
        if item_name in self.data["items"]:
            del self.data["items"][item_name]
            self.save_data()

    def search_item(self, search_term):
        return {k: v for k, v in self.data["items"].items() if search_term.lower() in k.lower()}

    def quick_sort(self, data, key_func, reverse=False):
        if len(data) <= 1:
            return data
        else:
            pivot = key_func(data[0])
            left = [item for item in data[1:] if (key_func(item) < pivot) != reverse]
            right = [item for item in data[1:] if (key_func(item) >= pivot) != reverse]
            return self.quick_sort(left, key_func, reverse) + [data[0]] + self.quick_sort(right, key_func, reverse)

    def get_sorted_items(self, by="name", reverse=False):
        items = self.get_all_items()
        if by == "name":
            return self.quick_sort(list(items.items()), key_func=lambda x: x[1]["name"].lower(), reverse=reverse)
        elif by == "price":
            return self.quick_sort(list(items.items()), key_func=lambda x: x[1]["price"], reverse=reverse)
        elif by == "stock":
            return self.quick_sort(list(items.items()), key_func=lambda x: int(x[1]["stock"]), reverse=reverse)
        else:
            return list(items.items())  
    
    def update_stock(self, item_name, new_stock):
        """
        Update stok barang
        
        Args:
            item_name: Nama barang yang akan diupdate stoknya
            new_stock: Stok baru
        """
        if item_name in self.data["items"]:
            self.data["items"][item_name]['stock'] = new_stock
            self.save_data()
            print(f"Stok {item_name} berhasil diupdate menjadi {new_stock}")
        else:
            print(f"Barang '{item_name}' tidak ditemukan")
    
    def get_available_stock(self, item_name, transaction_manager=None):
        """
        Menghitung stok yang tersedia berdasarkan data item dan transaksi
        
        Args:
            item_name: Nama barang
            transaction_manager: Instance TransactionManager untuk menghitung stok aktual
        
        Returns:
            int: Jumlah stok yang tersedia
        """
        item = self.get_item(item_name)
        if not item:
            return 0
        
        if transaction_manager:
            stock_calculation = transaction_manager.calculate_stock()
            return stock_calculation.get(item_name, int(item.get('stock', 0)))
        else:
            return int(item.get('stock', 0))