from rich.panel import Panel
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from module.Manager.UserManager import UserManager
from module.Manager.ItemsManager import ItemsManager
from module.Manager.TransactionManager import TransactionManager
from module.transaction import Transaction
import os

console = Console()
transaction = TransactionManager()

def validate_input(prompt_text, allow_empty=False, input_type="string", min_value=None, max_value=None):
    """
    Fungsi untuk memvalidasi input dari pengguna
    
    Args:
        prompt_text (str): Teks prompt yang ditampilkan
        allow_empty (bool): Apakah input kosong diperbolehkan
        input_type (str): Tipe input ("string", "int", "float")
        min_value (int/float): Nilai minimum (untuk angka)
        max_value (int/float): Nilai maksimum (untuk angka)
    Returns:
        str/int/float: Input yang sudah divalidasi
    """
    while True:
        user_input = input(prompt_text).strip()
        
        if not allow_empty and not user_input:
            console.print("[bold red]❌ Input tidak boleh kosong![/bold red]")
            continue
        
        if allow_empty and not user_input:
            return user_input
        
        if input_type == "int":
            try:
                value = int(user_input)
                if min_value is not None and value < min_value:
                    console.print(f"[bold red]❌ Nilai harus minimal {min_value}![/bold red]")
                    continue
                if max_value is not None and value > max_value:
                    console.print(f"[bold red]❌ Nilai harus maksimal {max_value}![/bold red]")
                    continue
                return value
            except ValueError:
                console.print("[bold red]❌ Input harus berupa angka![/bold red]")
                continue
        
        elif input_type == "float":
            try:
                value = float(user_input)
                if min_value is not None and value < min_value:
                    console.print(f"[bold red]❌ Nilai harus minimal {min_value}![/bold red]")
                    continue
                if max_value is not None and value > max_value:
                    console.print(f"[bold red]❌ Nilai harus maksimal {max_value}![/bold red]")
                    continue
                return value
            except ValueError:
                console.print("[bold red]❌ Input harus berupa angka desimal![/bold red]")
                continue
        
        return user_input


def user_main_menu(item_manager: ItemsManager, userManager: UserManager, transaction_manager: TransactionManager, username):
    while True:
        console.clear()
        console.print(Panel.fit(f"👋 [bold cyan]Selamat Datang, {username.capitalize()}![/bold cyan]\nGunakan dashboard ini untuk melihat dan membeli barang dengan mudah.\nSilakan pilih fitur yang ingin dijalankan:", title="Dashboard Pengguna"))
        console.print("""
[bold green]1.[/bold green] Lihat Daftar Barang
[bold green]2.[/bold green] Beli Barang
[bold green]3.[/bold green] Riwayat Pembelian
[bold green]4.[/bold green] Cari Barang
[bold green]5.[/bold green] Sorting Barang
[bold green]6.[/bold green] Keluar dari Aplikasi
""")

        pilihan = validate_input("Masukkan pilihan (1-6): ", input_type="int", min_value=1, max_value=6)

        if pilihan == 1:
            menu_daftar_barang(item_manager, transaction_manager)
        elif pilihan == 2:
            menu_beli_barang(transaction_manager, item_manager, username)
        elif pilihan == 3:
            menu_barang_dibeli(transaction_manager, username)
        elif pilihan == 4:
            menu_cari_barang(item_manager, transaction_manager)
        elif pilihan == 5:
            menu_sorting_barang(item_manager, transaction_manager)
        elif pilihan == 6:
            console.print("[bold red]Keluar dari aplikasi...[/bold red]")
            break


def menu_daftar_barang(item_manager, transaction_manager):
    items = item_manager.get_all_items()
    if items:
        table = Table(title="Daftar Barang")
        table.add_column("Nama Barang", style="cyan", justify="center")
        table.add_column("Kategori", style="magenta")
        table.add_column("Stok Tersedia", style="green")
        table.add_column("Harga", style="yellow")

        stock_calculation = transaction_manager.calculate_stock()

        for item_name, item in items.items():
            stok_tersedia = stock_calculation.get(item_name, int(item['stock']))
            table.add_row(
                item_name, 
                item['category'], 
                str(stok_tersedia),
                f"Rp {item['price']:,}"
            )

        console.print(table)
    else:
        console.print("[red]Tidak ada barang.[/red]")
    
    Prompt.ask("[bold yellow]Tekan enter untuk lanjut[/bold yellow]")


def menu_beli_barang(transaction_manager: TransactionManager, item_manager: ItemsManager, username: str):
    console.print("\n[bold green]-- Menu Beli Barang --[/bold green]")
    
    items = item_manager.get_all_items()
    if not items:
        console.print("[red]Tidak ada barang tersedia.[/red]")
        Prompt.ask("[bold yellow]Tekan enter untuk kembali[/bold yellow]")
        return

    stock_calculation = transaction_manager.calculate_stock()
    
    available_items = []
    for item_name, item in items.items():
        stok_tersedia = stock_calculation.get(item_name, int(item['stock']))
        if stok_tersedia > 0:
            item_copy = item.copy()
            item_copy['available_stock'] = stok_tersedia
            available_items.append(item_copy)

    if not available_items:
        console.print("[red]Tidak ada barang yang tersedia untuk dijual.[/red]")
        Prompt.ask("[bold yellow]Tekan enter untuk kembali[/bold yellow]")
        return

    table = Table(title="Daftar Barang Tersedia")
    table.add_column("No", style="cyan")
    table.add_column("Nama Barang")
    table.add_column("Stok Tersedia")
    table.add_column("Harga")

    for i, item in enumerate(available_items, start=1):
        table.add_row(
            str(i), 
            item["name"], 
            str(item["available_stock"]), 
            f'Rp {item["price"]:,}'
        )

    console.print(table)

    pilihan = validate_input(
        "Masukkan nomor barang yang ingin dibeli: ", 
        input_type="int", 
        min_value=1, 
        max_value=len(available_items)
    )
    
    barang = available_items[pilihan - 1]
    console.print(f"[cyan]Anda memilih: {barang['name']} (Stok: {barang['available_stock']})[/cyan]")
    
    jumlah = validate_input(
        "Jumlah yang ingin dibeli: ", 
        input_type="int", 
        min_value=1, 
        max_value=barang["available_stock"]
    )

    transaksi = Transaction(
        itemName=barang["name"],
        type="keluar",
        quantity=jumlah,
        supplier="",  
        pricePerItem=barang["price"],
        customer=username,
        notes="Pembelian oleh user"
    )
    
    transaction_manager.add_transaction(transaksi)

    total_harga = barang["price"] * jumlah
    console.print(f"[green]✅ Pembelian berhasil![/green]")
    console.print(f"[green]Barang: {barang['name']}[/green]")
    console.print(f"[green]Jumlah: {jumlah}[/green]") 
    console.print(f"[green]Total harga: Rp {total_harga:,}[/green]")
    
    Prompt.ask("[bold yellow]Tekan enter untuk kembali[/bold yellow]")


def menu_barang_dibeli(transaction_manager: TransactionManager, username: str):
    console.print("\n[bold blue]-- Riwayat Pembelian Barang Anda --[/bold blue]")
    transaksi = transaction_manager.get_all_transactions()

    transaksi_user = [t for t in transaksi if t["type"] == "keluar" and t.get("customer") == username]

    if not transaksi_user:
        console.print("[yellow]Anda belum pernah membeli barang.[/yellow]")
        Prompt.ask("[bold yellow]Tekan enter untuk kembali[/bold yellow]")
        return

    table = Table(
        title=f"\n 📦 Riwayat Pembelian - {username.capitalize()}",
        header_style="bold white",
        border_style="grey50",
        row_styles=["", "grey23"] 
    )

    table.add_column("No", style="bright_cyan", justify="center")
    table.add_column("Barang", style="white")
    table.add_column("Jumlah", style="bright_white", justify="center")
    table.add_column("Harga Satuan", style="white", justify="right")
    table.add_column("Total", style="bright_cyan", justify="right")
    table.add_column("Tanggal", style="white")

    total_pengeluaran = 0
    for i, t in enumerate(transaksi_user, start=1):
        tanggal = t["date"].split("T")[0] if "T" in t["date"] else t["date"]
        table.add_row(
            str(i),
            t["itemName"],
            str(t["quantity"]),
            f'Rp {t["pricePerItem"]:,}',
            f'Rp {t["totalPrice"]:,}',
            tanggal
        )
        total_pengeluaran += t["totalPrice"]

    console.print(table)
    console.print(f"\n[bold green]Total Pengeluaran: Rp {total_pengeluaran:,}[/bold green]")
    Prompt.ask("[bold yellow]Tekan enter untuk kembali[/bold yellow]")


def menu_cari_barang(item_manager, transaction_manager):
    console.print("\n[bold green]-- Cari Barang --[/bold green]")
    
    search_term = validate_input("Masukkan nama barang yang dicari: ", allow_empty=False)
    
    hasil = item_manager.search_item(search_term)
    
    if not hasil:
        console.print(f"[yellow]Tidak ditemukan barang dengan kata kunci '{search_term}'.[/yellow]")
        Prompt.ask("[bold yellow]Tekan enter untuk kembali[/bold yellow]")
        return
    
    table = Table(title=f"Hasil Pencarian: '{search_term}'")
    table.add_column("Nama Barang", style="cyan")
    table.add_column("Kategori", style="magenta")
    table.add_column("Stok Tersedia", style="green")
    table.add_column("Harga", style="yellow")
    
    stock_calculation = transaction_manager.calculate_stock()
    
    for item_name, item in hasil.items():
        stok_tersedia = stock_calculation.get(item_name, int(item['stock']))
        table.add_row(
            item_name,
            item['category'],
            str(stok_tersedia),
            f"Rp {item['price']:,}"
        )
    
    console.print(table)
    Prompt.ask("[bold yellow]Tekan enter untuk kembali[/bold yellow]")


def menu_sorting_barang(item_manager, transaction_manager):
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        console.print("\n[bold green]-- Sorting Barang --[/bold green]")
        console.print("""
    [bold green]1.[/bold green] Urutkan berdasarkan Nama (A-Z)
    [bold green]2.[/bold green] Urutkan berdasarkan Harga (Termurah)
    [bold green]3.[/bold green] Urutkan berdasarkan Harga (Termahal)
    [bold green]4.[/bold green] Urutkan berdasarkan Stok (Terkecil)
    [bold green]5.[/bold green] Urutkan berdasarkan Stok (Terbanyak)
    [bold green]6.[/bold green] Kembali
    """)
        pilihan = validate_input("Pilih sorting (1-6): ", input_type="int", min_value=1, max_value=6)

        items = item_manager.get_all_items()
        if not items:
            console.print("[red]Tidak ada barang untuk diurutkan.[/red]")
            Prompt.ask("[bold yellow]Tekan enter untuk kembali[/bold yellow]")
            return

        stock_calculation = transaction_manager.calculate_stock()

        if pilihan == 1:
            sorted_items = item_manager.get_sorted_items(by="name", reverse=False)
            title = "Barang Diurutkan berdasarkan Nama (A-Z)"
        elif pilihan == 2:
            sorted_items = item_manager.get_sorted_items(by="price", reverse=False)
            title = "Barang Diurutkan berdasarkan Harga (Termurah)"
        elif pilihan == 3:
            sorted_items = item_manager.get_sorted_items(by="price", reverse=True)
            title = "Barang Diurutkan berdasarkan Harga (Termahal)"
        elif pilihan == 4:
            sorted_items = item_manager.get_sorted_items(by="stock", reverse=False, stock_data=stock_calculation)
            title = "Barang Diurutkan berdasarkan Stok (Terkecil)"
        elif pilihan == 5:
            sorted_items = item_manager.get_sorted_items(by="stock", reverse=True, stock_data=stock_calculation)
            title = "Barang Diurutkan berdasarkan Stok (Terbanyak)"
        elif pilihan == 6:
            return

        table = Table(title=title)
        table.add_column("Nama Barang", style="cyan")
        table.add_column("Kategori", style="magenta")
        table.add_column("Stok Tersedia", style="green")
        table.add_column("Harga", style="yellow")

        for item_name, item in sorted_items:
            stok_tersedia = stock_calculation.get(item_name, int(item['stock']))
            table.add_row(
                item_name,
                item['category'],
                str(stok_tersedia),
                f"Rp {item['price']:,}"
            )

        console.print(table)
        Prompt.ask("[bold yellow]Tekan enter untuk kembali[/bold yellow]")
        
if __name__ == "__main__":
    user_main_menu()