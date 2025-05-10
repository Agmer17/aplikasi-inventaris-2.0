# dashboard_employee.py
from rich.panel import Panel
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from module.Manager.UserManager import UserManager
from module.Manager.ItemsManager import ItemsManager
from module.dashboard import Util
from module.Manager.TransactionManager import TransactionManager

console = Console()
transaction = TransactionManager()

def user_main_menu(item_manager: ItemsManager, userManager:UserManager, currentUser) -> None:
    while True:
        console.clear()
        console.print(Panel.fit("👋 [bold cyan]Selamat datang, Pengguna![/bold cyan]\nGunakan dashboard ini untuk mengelola data barang dan laporan dengan mudah.\nPilih fitur yang ingin dijalankan:", title="Dashboard Pengguna"))
        console.print("""
[bold green]1.[/bold green] Lihat Daftar Barang
[bold green]2.[/bold green] Beli Barang
[bold green]3.[/bold green] Lihat Barang yang dibeli
[bold green]4.[/bold green] Cari Barang
[bold green]5.[/bold green] Sorting Barang
[bold green]6.[/bold green] Keluar App
""")
        pilihan = input("Masukkan pilihan (1-6): ")

        if pilihan == "1":
            menu_daftar_barang(item_manager)
        elif pilihan == "2":
            menu_pinjam_barang(item_manager, currentUser)
        elif pilihan == "3":
            menu_barang_dipinjam(transaction, currentUser.username)
        elif pilihan == "4":
            menu_cari_barang()
        elif pilihan == "5":
            menu_soting_barang()
        elif pilihan == "6":
            console.print("[bold red]Keluar dari aplikasi...[/bold red]")
            break
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")


def menu_daftar_barang(item_manager:ItemsManager):
    Util.printTable("daftar items", item_manager, "items")
    Prompt.ask("[bold yellow] tekan enter untuk lanjut[/bold yellow]")

def menu_pinjam_barang(item_Manager:ItemsManager, currentUser):
    console.clear()
    Util.printTable("daftar barang", item_Manager, "items")
    itemNameToBuy = Prompt.ask("Masukan nama barang yg ingin dibeli ")
    itemToBuy = item_Manager.get_item(itemNameToBuy)
    
    if itemNameToBuy : 
        amount = int(Prompt.ask(f"Masukan jumlah item yang ingin dibeli "))
        old_stock = int(itemToBuy["stock"])
        
        if amount <= old_stock : 
            newStock = old_stock - amount
            Util.createTransaction(itemToBuy["name"], old_stock, newStock, itemToBuy["supplier"], itemToBuy["price"], transaction, "pembelian barang", currentUser.username)
            
            itemToBuy["stock"] = newStock
            item_Manager.update_item(itemToBuy["name"], itemToBuy)
            console.print("[bold green]pembelian berhasil dilakukan[/bold green]")
            Prompt.ask("[bold green]TEKAN ENTER[/bold green]")
            
        else : 
            console.print("[bold red]JUMLAH YANG DIMASUKKAN TIDAK VALID! TRANSAKSI DIBATALKAN![/bold red]")
            Prompt.ask("[ENTER]")
    else : 
        console.print("[bold red]Barang tidak ditemukan![/bold red]")
        Prompt.ask("[ENTER]")

def menu_barang_dipinjam(transactions: TransactionManager, username:str) -> None:
    Util.displayTrByUser(transactions.getTransactionByUser(username))
    Prompt.ask("[bold green][ENTER][/bold green]")
def menu_cari_barang():
   pass
def menu_barang_employee():
   pass
def menu_soting_barang():
   pass

if __name__ == "__main__":
    user_main_menu()
