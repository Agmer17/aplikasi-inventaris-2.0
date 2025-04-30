# dashboard_employee.py
from rich.panel import Panel
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from module.Manager.UserManager import UserManager
from module.Manager.ItemsManager import ItemsManager

console = Console()

def user_main_menu(item_manager: ItemsManager, userManager:UserManager) -> None:
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
            menu_pinjam_barang()
        elif pilihan == "3":
            menu_barang_dipinjam()
        elif pilihan == "4":
            menu_cari_barang()
        elif pilihan == "5":
            menu_soting_barang()
        elif pilihan == "6":
            console.print("[bold red]Keluar dari aplikasi...[/bold red]")
            break
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")


def menu_daftar_barang(item_manager):
    items = item_manager.get_all_items()
    if items:
        table = Table(title="Daftar Barang")
        table.add_column("Nama Barang", style="cyan", justify="center")
        table.add_column("Kategori", style="magenta")
        table.add_column("Stok", style="green")

        for item_name, item in items.items():
            table.add_row(item_name, item['category'], str(item['stock']))

            console.print(table)
            Prompt.ask("[bold yellow] tekan enter untuk lanjut[/bold yellow]")
    else:
        print("Tidak ada barang.")

def menu_pinjam_barang():
   pass

def menu_barang_dipinjam():
   pass
def menu_cari_barang():
   pass
def menu_barang_employee():
   pass
def menu_soting_barang():
   pass

if __name__ == "__main__":
    user_main_menu()
