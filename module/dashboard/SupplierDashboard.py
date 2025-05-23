# dashboard_employee.py
from rich.console import Console
from rich.panel import Panel

console = Console()

def supplier_main_menu():
    while True:
        console.clear()
        console.print(Panel.fit("👋 [bold cyan]Selamat datang, Supplier![/bold cyan]\nGunakan dashboard ini untuk mengelola semua data barang dan laporan dengan mudah.\nPilih fitur yang ingin dijalankan:", title="Dashboard Supplier"))
        console.print("""
[bold green]1.[/bold green] Barang
[bold green]2.[/bold green] Laporan
[bold green]3.[/bold green] Keluar App
""")
        pilihan = input("Masukkan pilihan (1-3): ")

        if pilihan == "1":
            menu_barang_employee()
        elif pilihan == "2":
            menu_laporan()
        elif pilihan == "3":
            console.print("[bold red]Keluar dari aplikasi...[/bold red]")
            break
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")

def menu_barang_employee():
    while True:
        console.clear()
        console.print(Panel.fit("👋 [bold cyan]Selamat datang, Karyawan![/bold cyan]\nGunakan dashboard ini untuk mengelola semua data barang, pengguna, dan laporan dengan mudah.\nPilih fitur yang ingin dijalankan:", title="Dashboard Karyawan"))
        console.print("""
[bold green]1.[/bold green] Tambah Barang
[bold green]2.[/bold green] Edit Barang
[bold green]3.[/bold green] Lihat Daftar Barang
[bold green]4.[/bold green] Cari
[bold green]5.[/bold green] Sorting
[bold green]6.[/bold green] Kembali                     
""")
        pilihan = input("Masukkan pilihan (1-6): ")
        if pilihan == "1":
            pass
        elif pilihan == "2":
            pass
        elif pilihan == "3":
            pass
        elif pilihan == "4":
            pass
        elif pilihan == "5":
            pass
        elif pilihan == "6":
            pass
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")

            console.print("[bold red]Pilihan tidak valid![/bold red]")

def menu_laporan():
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]Menu Laporan[/bold cyan]"))
        console.print("""
1. Laporan Daftar Barang
2. Laporan Transaksi Barang
3. Kembali
""")
        p = input("Pilih menu: ")
        if p == "3":
            break
        
if __name__ == "__main__":
    supplier_main_menu()
