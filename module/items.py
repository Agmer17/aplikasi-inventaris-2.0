import datetime
from module.User import Supplier  # Misal Supplier didefinisikan di file lain

class Item:
    """
    Kelas untuk merepresentasikan sebuah item/barang dalam sistem.

    Atribut:
    - name (str): Nama item
    - category (str): Kategori item
    - stock (int): Jumlah stok item
    - price (float): Harga beli item
    - sellPrice (float): Harga jual item
    - desc (str): Deskripsi item
    - supplier (Supplier): Object Supplier yang menyediakan item
    - status (str): Status item (misal 'available', 'out_of_stock')
    - entrydate (datetime.datetime): Tanggal item dimasukkan ke sistem (default: waktu sekarang)
    """

    def __init__(
        self,
        name: str,
        category: str,
        stock: int,
        price: float,
        sellPrice: float,
        desc: str,
        supplier: Supplier,
        status: str,
        entrydate: datetime.datetime = datetime.datetime.now()
    ):
        self.name = name
        self.category = category
        self.stock = stock
        self.price = price
        self.sellPrice = sellPrice

        if isinstance(entrydate, str):
            self.entrydate = datetime.datetime.strptime(entrydate, "%Y-%m-%dT%H:%M:%S.%fZ")
        elif isinstance(entrydate, datetime.datetime):
            self.entrydate = entrydate
        else:
            self.entrydate = datetime.datetime.now()

        self.desc = desc
        self.supplier = supplier
        self.status = status
    
    def getAllData(self):
        """
        Mengubah object Item menjadi dictionary agar bisa disimpan ke JSON atau ditampilkan di menu.
        """
        return {
            "name": self.name,
            "category": self.category,
            "stock": self.stock,
            "price": self.price,
            "sellPrice": self.sellPrice,
            "desc": self.desc,
            "supplier": self.supplier.getAllData(),  # asumsi Supplier juga punya to_dict(). Jadi nanti di supplier itu ada method get data buat ambil semua data dari seorang supplier
            "status": self.status,
            "entrydate": self.entrydate.isoformat() + "Z"  # format ISO untuk konsistensi
        }

