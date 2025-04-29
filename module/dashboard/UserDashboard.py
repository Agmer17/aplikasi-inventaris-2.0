# dashboard_employee.py
from rich.console import Console
from rich.panel import Panel

console = Console()

def user_main_menu():
    while True:
        console.clear()
        console.print(Panel.fit("👋 [bold cyan]Selamat datang, Pengguna![/bold cyan]\nGunakan dashboard ini untuk mengelola data barang dan laporan dengan mudah.\nPilih fitur yang ingin dijalankan:", title="Dashboard Pengguna"))
        console.print("""
[bold green]1.[/bold green] Lihat Daftar Barang
[bold green]2.[/bold green] Pinjam Barang
[bold green]3.[/bold green] Lihat Barang yang Dipinjam
[bold green]4.[/bold green] Cari Barang
[bold green]5.[/bold green] Sorting Barang
[bold green]6.[/bold green] Keluar App
""")
        pilihan = input("Masukkan pilihan (1-6): ")

        if pilihan == "1":
            menu_barang_employee()
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


def menu_barang_employee():
   pass

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
