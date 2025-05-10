from module.Manager.ItemsManager import ItemsManager
from module.Manager.UserManager import UserManager
from rich.table import Table
from rich.console import Console
from module.transaction import Transaction
from rich.panel import Panel
from collections import defaultdict
from rich.prompt import Prompt


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

def editAllData(name: str, listData: UserManager | ItemsManager, fields:dict) :
    if isinstance(listData, UserManager) : 
        for key, prompt_text in fields.items():
            new_value = Prompt.ask(prompt_text)
            if new_value:
                listData.editUser(name, key, new_value)
        return
    
    if isinstance(listData, ItemsManager) : 
        editedItems = listData.get_item(name)
        
        if editedItems : 
            for key, val in fields.items() :
                new_value = Prompt.ask(val)
                if new_value : 
                    editedItems[key] = new_value
            listData.update_item(name, editedItems)
        
        return editedItems
    pass

def createTransaction(
    item_name: str,
    stok_awal: int,
    stok_baru: int,
    supplier: str,
    price_per_item: float,
    transaction_manager,
    reason: str = "Perubahan stok", 
    customer: str|None = None
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
        "customer": customer,
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

def displayTrByUser(listOfTransaction: list) -> None : 
    table = Table(title="Daftar Transaksi Barang", show_lines=True)
    console = Console()
    
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
    
    for data in listOfTransaction:
        trx = data.getAllData()
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



def generate_transaction_report_rich(transactionsManager):
    console = Console()
    transactions = transactionsManager.get_all_transactions()
    # Ringkasan
    total_items = 0
    total_value = 0
    masuk_count = 0
    keluar_count = 0
    quantity_per_item = defaultdict(int)

    # TABEL TRANSAKSI
    table = Table(title="📦 Laporan Transaksi Barang", show_lines=False, expand=True)
    table.add_column("ID", style="cyan", no_wrap=True, width=8)
    table.add_column("Barang", style="bold", width=15)
    table.add_column("Tipe", style="green", width=7)
    table.add_column("Qty", justify="right", width=4)
    table.add_column("Harga", justify="right", width=12)
    table.add_column("Total", justify="right", width=14)
    table.add_column("Tanggal", style="dim", width=16)
    table.add_column("Supplier", style="magenta", width=10)
    table.add_column("Catatan", style="yellow", width=20)

    for trx in transactions:
        id_short = trx["id"][:8]
        name = trx["itemName"]
        tipe = trx["type"]
        qty = trx["quantity"]
        harga = f"Rp {trx['pricePerItem']:,.0f}"
        total = f"Rp {trx['totalPrice']:,.0f}"
        tgl = trx["date"][:16]
        supplier = trx.get("supplier") or "-"
        notes = trx.get("notes") or "-"

        table.add_row(id_short, name, tipe, str(qty), harga, total, tgl, supplier, notes)

        # Ringkasan data
        total_items += qty
        total_value += trx["totalPrice"]
        quantity_per_item[name] += qty
        if tipe == "masuk":
            masuk_count += 1
        elif tipe == "keluar":
            keluar_count += 1

    # Cetak tabel
    console.print(table)

    # Ringkasan
    summary_panel = Panel.fit(
        f"[bold green]Total transaksi:[/bold green] {len(transactions)}\n"
        f"[green]Masuk:[/green] {masuk_count}   [red]Keluar:[/red] {keluar_count}\n"
        f"[bold blue]Total barang:[/bold blue] {total_items}\n"
        f"[bold blue]Total nilai transaksi:[/bold blue] Rp {total_value:,.0f}",
        title="📈 Ringkasan",
        border_style="blue"
    )
    console.print(summary_panel)

    # BAR CHART JUMLAH BARANG
    if quantity_per_item: # Pastikan ada data sebelum menghitung max
        max_len = max(len(name) for name in quantity_per_item)
        max_qty = max(quantity_per_item.values())
        bar_size = 30 # Lebar maksimum bar dalam karakter

        if max_qty == 0: # Hindari pembagian dengan nol jika semua qty adalah 0
            max_qty = 1 # Atur max_qty ke 1 agar bar tetap terlihat (atau bisa diubah logikanya)

        for name, qty in quantity_per_item.items():
            # Hitung panjang bar berdasarkan proporsi qty terhadap max_qty
            bar_length = int((qty / max_qty) * bar_size)
            # Buat string bar menggunakan karakter blok '█'
            bar_string = '█' * bar_length
            # Tambahkan spasi di belakang bar agar panjang totalnya bar_size (opsional, untuk alignment visual)
            # padding = ' ' * (bar_size - bar_length)
            # Aplikasikan warna cyan menggunakan sintaks rich
            colored_bar = f"[cyan]{bar_string}[/cyan]"

            # Format label nama item agar rata kiri dengan panjang max_len
            label = f"{name:<{max_len}}"

            # Cetak label, bar, dan kuantitas
            console.print(f"{label} {colored_bar} {qty}")
