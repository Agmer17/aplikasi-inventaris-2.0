import datetime

"""
Bentuk data json dari transaksi : 

[
  {
    "id": "TRX001",
    "itemName": "Televisi",
    "type": "penjualan",
    "quantity": 2,
    "pricePerItem": 3000000,
    "totalPrice": 6000000,
    "date": "2025-05-01T10:25:00",
    "customer": "Budi",
    "notes": "Pembayaran tunai"
  },
  {
    "id": "TRX002",
    "itemName": "Kipas Angin",
    "type": "pembelian",
    "quantity": 5,
    "pricePerItem": 150000,
    "totalPrice": 750000,
    "date": "2025-05-01T11:10:00",
    "supplier": "PT Elektronik Sejuk",
    "notes": "Pembelian rutin bulanan"
  }
]
"""

class Transaction:
    def __init__(
        self,
        id: str,
        itemName: str,
        type: str,
        quantity: int,
        supplier: str,
        pricePerItem: float,
        date: str|None = None,
        customer: str|None = None,
        notes: str|None = None
    ):
        self.id: str = id  # ID unik transaksi
        self.itemName: str = itemName  # Nama barang dalam transaksi
        self.type: str = type  # Jenis transaksi ("keluar" atau "masuk")
        self.quantity: int = quantity  # Jumlah barang dalam transaksi
        self.pricePerItem: float = pricePerItem  # Harga per item
        self.totalPrice: float = quantity * pricePerItem  # Total harga transaksi
        self.date: str = date or datetime.now().isoformat()  # Tanggal transaksi
        self.customer: str|None = customer if type == "keluar" else None  # Isi jika "keluar"
        self.supplier: str = supplier
        self.notes: str|None = notes  # Catatan transaksi