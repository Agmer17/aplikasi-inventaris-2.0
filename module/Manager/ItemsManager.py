import json
import os
from datetime import datetime
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
        with open('data/items.json', 'w') as f:
            json.dump(self.data, f, indent=4)

    # CRUD untuk Categories
    def get_all_categories(self):
        categories = self.data.get("categories", {})
        print("Categories:", categories)
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
        if item_name in self.data["items"]:
            self.data["items"][item_name] = item_data
            self.save_data()

    def delete_item(self, item_name):
        if item_name in self.data["items"]:
            del self.data["items"][item_name]
            self.save_data()

    def search_item(self, search_term):
        return {k: v for k, v in self.data["items"].items() if search_term.lower() in k.lower()}

    def sort_items(self, sort_by):
        sorted_items = sorted(self.data["items"].items(), key=lambda x: x[1][sort_by])
        return dict(sorted_items)