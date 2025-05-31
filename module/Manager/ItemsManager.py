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
        """
            Menyimpan data item dan kategori ke file JSON di folder 'data'
        """

        os.makedirs('data', exist_ok=True)
        with open('data/items.json', 'w') as f:
            json.dump(self.data, f, indent=4)

    def get_all_categories(self):
        """
            Mengambil semua kategori dari data

            Returns:
                dict: Dictionary berisi semua kategori
        """

        categories = self.data.get("categories", {})
        return categories

    def add_category(self, category_name):
        """
            Menambahkan kategori baru ke dalam data

            Args:
                category_name (str): Nama kategori yang akan ditambahkan
        """

        category_id = str(len(self.data["categories"]) + 1)
        self.data["categories"][category_id] = category_name
        self.save_data()

    def edit_category(self, category_id, new_name):
        """
            Mengubah nama kategori berdasarkan ID

            Args:
                category_id (str): ID kategori yang akan diubah
                new_name (str): Nama baru untuk kategori
        """

        if category_id in self.data["categories"]:
            self.data["categories"][category_id] = new_name
            self.save_data()

    def delete_category(self, category_id):
        """
            Menghapus kategori dari data berdasarkan ID

            Args:
                category_id (str): ID kategori yang akan dihapus
        """

        if category_id in self.data["categories"]:
            del self.data["categories"][category_id]
            self.save_data()

    def get_all_items(self):
        """
            Mengambil semua item dari data

            Returns:
                dict: Dictionary berisi semua item
        """

        return self.data.get("items", {})

    def get_item(self, item_name):
        """
            Mengambil data item berdasarkan nama

            Args:
                item_name (str): Nama item yang ingin diambil datanya

            Returns:
                dict or None: Data item jika ditemukan, None jika tidak ada
        """

        return self.data["items"].get(item_name)

    def add_item(self, item_name, item_data):
        """
            Menambahkan item baru ke dalam data

            Args:
                item_name (str): Nama item
                item_data (dict): Informasi item (kategori, harga, stok, dll.)
        """

        self.data["items"][item_name] = item_data
        self.save_data()

    def update_item(self, item_name, item_data):
        """
            Menambahkan item baru ke dalam data

            Args:
                item_name (str): Nama item
                item_data (dict): Informasi item (kategori, harga, stok, dll.)
        """

        items = self.data["items"]
        
        new_name = item_data["name"]
        if item_name != new_name:
            if new_name in items:
                print("Item dengan nama baru sudah ada!")  
                return
            del items[item_name]
        
        items[new_name] = item_data
        self.save_data()

    def delete_item(self, item_name: str):
        """
        Menghapus item dari data berdasarkan nama.

        Args:
            item_name (str): Nama item yang akan dihapus.
        """
        if item_name in self.data["items"]:
            del self.data["items"][item_name]
            self.save_data()
        else:
            raise ValueError("Item tidak ditemukan.")


    def search_item(self, search_term):
        """
            Mencari item berdasarkan kata kunci nama secara linier

            Args:
                search_term (str): Kata kunci pencarian

            Returns:
                dict: Dictionary berisi item yang cocok dengan kata kunci
        """
        hasil = {}
        for nama, info in self.data["items"].items():
            if search_term.lower() in nama.lower():
                hasil[nama] = info
        return hasil


    def quick_sort(self, data, key_func, reverse=False):
        """
            Mengurutkan data menggunakan algoritma Quick Sort

            Args:
                key_func (function): Fungsi untuk menentukan nilai yang dibandingkan
                reverse (bool): Jika True, urutan akan dibalik (descending)

            Returns:
                list: Data yang sudah diurutkan
        """

        if len(data) <= 1:
            return data
        else:
            pivot = key_func(data[0])
            left = [item for item in data[1:] if (key_func(item) < pivot) != reverse]
            right = [item for item in data[1:] if (key_func(item) >= pivot) != reverse]
            return self.quick_sort(left, key_func, reverse) + [data[0]] + self.quick_sort(right, key_func, reverse)

    def get_sorted_items(self, by="name", reverse=False, stock_data=None):
        """
        Mengembalikan daftar barang yang sudah diurutkan

        Args:
            by (str): Kriteria pengurutan. Bisa berupa "name", "price", atau "stock".
            reverse (bool): Jika True, maka urutan dibalik (misalnya Z-A atau harga termahal duluan).
            stock_data (dict, optional): Data stok aktual dari transaksi (jika ingin mengurut berdasarkan stok terkini).

        Returns:
            list: Daftar barang dalam format list of tuples (item_name, item_data) yang sudah diurutkan sesuai kriteria.
        """

        items = self.get_all_items()
        item_list = list(items.items())

        if by == "name":
            key_func = lambda x: x[1]["name"].lower()
        elif by == "price":
            key_func = lambda x: (x[1]["price"], x[1]["name"].lower())
        elif by == "stock":
            key_func = lambda x: (stock_data.get(x[0], int(x[1]["stock"])) if stock_data else int(x[1]["stock"]), x[1]["name"].lower())
        else:
            return item_list 

        return self.quick_sort(item_list, key_func=key_func, reverse=reverse)

    
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