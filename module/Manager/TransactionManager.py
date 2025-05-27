from module.transaction import Transaction
import json
import os

class TransactionManager:
    """
    Mengelola transaksi antara user dan item.

    Fitur:
    - Tambah transaksi baru
    - Lihat riwayat transaksi
    - Load dan simpan data ke file JSON
    - Menyimpan data transaksi yang di load dari json
    """
    def __init__(self, filename: str = "data/transaksi.json"):
        self.path = filename
        # Buat direktori jika belum ada
        # Load transaksi dari file jika ada
        self.transactions = self.load_transactions_from_json(filename)
    
    def add_transaction(self, transaction: Transaction) -> None:
        """
        Menambahkan transaksi baru ke daftar, dengan pengecekan stok jika type == 'keluar'.
        
        Args:
            transaction: Objek Transaction yang akan ditambahkan
        """
        if transaction.type == "keluar":
            stock = self.calculate_stock()
            item_stock = stock.get(transaction.itemName, 0)

            if transaction.quantity > item_stock:
                print(f"❌ Gagal menambahkan transaksi keluar: Stok '{transaction.itemName}' hanya {item_stock}, "
                    f"tidak cukup untuk mengurangi {transaction.quantity}.")
                return
        
        # Jika type masuk, atau type keluar tapi stok cukup
        self.transactions.append(transaction)
        print(f"✅ Transaksi {transaction.id} berhasil ditambahkan")
        self.save_transactions()
    
    def get_all_transactions(self) -> list[Transaction]:
        """
        Mendapatkan semua transaksi
        
        Returns:
            list[Transaction]: Daftar semua transaksi
        """
        temp = []
        for data in self.transactions :
            temp.append(data.getAllData())
        return temp
    
    def save_transactions(self) -> None:
        """
        Menyimpan semua transaksi ke file JSON
        """
        self.write_transactions_to_json(self.transactions, self.path)
    
    def write_transactions_to_json(self, transactions: list[Transaction], filename: str = None) -> None:
        """
        Menulis daftar objek Transaction ke file JSON
        
        Args:
            transactions: Daftar objek Transaction
            filename: Nama file JSON yang akan dibuat (opsional)
        """
        if filename is None:
            filename = self.path
            
        # Konversi daftar objek Transaction menjadi daftar dictionary
        transactions_data = [transaction.getAllData() for transaction in transactions]
        
        # Tulis ke file JSON
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(transactions_data, file, indent=4, ensure_ascii=False)
        
        print(f"Data transaksi berhasil disimpan ke {filename}")

    @staticmethod
    def load_transactions_from_json(filename: str) -> list[Transaction]:
        """
        Memuat data transaksi dari file JSON dan mengkonversinya menjadi objek Transaction
        
        Args:
            filename: Nama file JSON yang akan dibaca
            
        Returns:
            list[Transaction]: Daftar objek Transaction
        """
        try:
            if not os.path.exists(filename):
                print(f"File {filename} tidak ditemukan. Membuat file baru.")
                # Buat file kosong dengan array JSON kosong
                with open(filename, 'w', encoding='utf-8') as file:
                    json.dump([], file)
                return []
                
            with open(filename, 'r', encoding='utf-8') as file:
                transactions_data = json.load(file)
            
            # Konversi setiap dictionary menjadi objek Transaction
            transactions = []
            for data in transactions_data:
                try:
                    transaction = Transaction(
                        itemName=data['itemName'],
                        type=data['type'],
                        quantity=data['quantity'],
                        supplier=data.get('supplier', ""),  # Default kosong jika tidak ada
                        pricePerItem=data['pricePerItem'],
                        date=data.get('date'),
                        customer=data.get('customer'),  
                        notes=data.get('notes'),
                        id=data.get('id')  
                    )
                    transactions.append(transaction)
                except KeyError as e:
                    print(f"Data transaksi tidak valid: {e}. Data yang ditemukan: {data}")
                    continue
            
            print(f"Berhasil memuat {len(transactions)} transaksi dari {filename}")
            return transactions
        
        except FileNotFoundError:
            print(f"File {filename} tidak ditemukan. Membuat daftar kosong.")
            return []
        except json.JSONDecodeError:
            print(f"Format file {filename} tidak valid. Membuat daftar kosong.")
            return []
        except Exception as e:
            print(f"Terjadi kesalahan saat memuat transaksi: {str(e)}")
            return []

    def calculate_stock(self) -> dict:
        """
        Menghitung stok akhir untuk setiap item berdasarkan transaksi masuk & keluar.
        Returns:
            dict: itemName -> sisa stok
        """
        stock = {}
        for trx in self.transactions:
                name = trx.itemName
                qty = trx.quantity

                if name not in stock:
                    stock[name] = 0

                if trx.type == "masuk":
                    stock[name] += qty
                elif trx.type == "keluar":
                    stock[name] -= qty

        return stock

