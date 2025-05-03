from module.Manager.ItemsManager import ItemsManager
from module.Manager.UserManager import UserManager
from rich.table import Table
from rich.console import Console
from module.transaction import Transaction


def userTable(title: str, data: UserManager, role: str) -> Table:
    temp: dict = data.getDataByRole(role)
    table = Table(title=title)
    table.add_column("Username", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Email", style="blue")
    table.add_column("Role", style="magenta")
    
    # Loop untuk menambahkan baris ke tabel
    for username, user in temp.items():
        table.add_row(username, user.name, user.email, user.role)
    
    return table


def itemTable(title:str, itemData:ItemsManager, type:str)  -> Table :
    
    if type == "items" : 
        items = itemData.get_all_items()
        table = Table(title=title)
        table.add_column("Nama Barang", style="cyan", justify="center")
        table.add_column("Kategori", style="magenta")
        table.add_column("Stok", style="green")

        for item_name, item in items.items():
            table.add_row(item_name, item['category'], str(item['stock']))
        return table

    elif type == "categories" : 
        # catgory table
        categoryTable = Table(title="Daftar Kategori")
        categoryTable.add_column("ID", style="cyan", justify="center")
        categoryTable.add_column("Nama Kategori", style="green")
        for category_id, category_name in itemData.get_all_categories().items():
            categoryTable.add_row(str(category_id), category_name)
            # -----------------------
        return categoryTable

def printTable(title: str, data: ItemsManager | UserManager, role: str | None) -> None:
    console = Console()
    
    # Validasi input tipe data
    if not (isinstance(data, ItemsManager) or isinstance(data, UserManager)):
        raise ValueError("Input gak valid! tolong masukan tipe data item atau user!")
    
    # Cek tipe data dan panggil fungsi yang sesuai
    if isinstance(data, UserManager):
        table = userTable(title, data, role)
        console.print(table)  # Cetak tabel
    else:
        
        if role not in ["categories", "items"] :
            raise ValueError("Input role gak valid! harap masukan items/category")
        items = itemTable(title, data, role)
        console.print(items)
        pass

def get_input_with_default(prompt, default_value, convert_type=None):
        user_input = input(f"{prompt} ({default_value}): ") or default_value
        if convert_type and user_input != default_value:
            return convert_type(user_input)
        return user_input if convert_type is None else convert_type(user_input)

def createTransaction(
    item_name: str,
    stok_awal: int,
    stok_baru: int,
    supplier: str,
    price_per_item: float,
    transaction_manager,
    reason: str = "Perubahan stok"
):
    console = Console()
    """
    Fungsi generik untuk membuat dan mencatat transaksi stok otomatis.
    
    Parameters:
    - item_name (str): Nama item.
    - stok_awal (int): Stok sebelum perubahan.
    - stok_baru (int): Stok setelah perubahan.
    - supplier (str): Nama supplier.
    - price_per_item (float): Harga per item.
    - transaction_manager: Objek manajer transaksi.
    - reason (str): Alasan perubahan stok, digunakan sebagai catatan transaksi.
    """
    selisih = stok_baru - stok_awal

    transaksi_data = {
        "itemName": item_name,
        "type": "masuk" if selisih > 0 else "keluar",
        "quantity": abs(selisih),
        "supplier": supplier,
        "pricePerItem": price_per_item,
        "customer": None,
        "notes": reason
    }

    data_transaksi = Transaction(**transaksi_data)
    transaction_manager.add_transaction(data_transaksi)

    console.print(f"[bold blue]Transaksi otomatis ({transaksi_data['type']}) tercatat sebanyak {transaksi_data['quantity']} unit.[/bold blue]")


def display_transactions(transactionManager):
    table = Table(title="Daftar Transaksi Barang", show_lines=True)
    console = Console()
    
    transactions = transactionManager.get_all_transactions()

    table.add_column("ID", style="cyan", no_wrap=True, max_width=10)
    table.add_column("Barang", style="bold", max_width=15)
    table.add_column("Tipe", style="green", width=6)
    table.add_column("Qty", justify="right", width=5)
    table.add_column("Harga", justify="right", width=12)
    table.add_column("Total", justify="right", width=12)
    table.add_column("Tgl", style="dim", width=16)
    table.add_column("Sup", style="magenta", max_width=10)
    table.add_column("Cus", style="magenta", max_width=10)
    table.add_column("Catatan", style="yellow", max_width=20)

    for trx in transactions:
        table.add_row(
            trx["id"],
            trx["itemName"],
            trx["type"],
            str(trx["quantity"]),
            f"Rp {trx['pricePerItem']:,.0f}",
            f"Rp {trx['totalPrice']:,.0f}",
            trx["date"],
            trx.get("supplier", "-") or "-",
            trx.get("customer", "-") or "-",
            trx.get("notes", "-") or "-"
        )

    console.print(table)
