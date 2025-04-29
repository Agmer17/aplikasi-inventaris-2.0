# dashboard_employee.py
from rich.console import Console
from rich.panel import Panel

console = Console()

def employee_main_menu():
    while True:
        console.clear()
        console.print(Panel.fit("👋 [bold cyan]Selamat datang, Karyawan![/bold cyan]\nGunakan dashboard ini untuk mengelola semua data barang, pengguna, dan laporan dengan mudah.\nPilih fitur yang ingin dijalankan:", title="Dashboard Karyawan"))
        console.print("""
[bold green]1.[/bold green] Barang
[bold green]2.[/bold green] Supplier
[bold green]3.[/bold green] Peminjam
[bold green]4.[/bold green] Laporan
[bold green]5.[/bold green] Keluar App
""")
        pilihan = input("Masukkan pilihan (1-5): ")

        if pilihan == "1":
            menu_barang_employee()
        elif pilihan == "2":
            menu_supplier_employee()
        elif pilihan == "3":
            menu_peminjam_employee()
        elif pilihan == "4":
            menu_laporan_employee()
        elif pilihan == "5":
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
def menu_supplier_employee():
    while True:
        console.clear()
        console.print(Panel.fit("👋 [bold cyan]Selamat datang, Karyawan![/bold cyan]\nGunakan dashboard ini untuk mengelola semua data barang, pengguna, dan laporan dengan mudah.\nPilih fitur yang ingin dijalankan:", title="Dashboard Karyawan"))
        console.print("""
[bold green]1.[/bold green] Edit Supplier
[bold green]2.[/bold green] Hapus Supplier
[bold green]3.[/bold green] Lihat Daftar Supplier
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
def menu_peminjam_employee():
    while True:
        console.clear()
        console.print(Panel.fit("👋 [bold cyan]Selamat datang, Karyawan![/bold cyan]\nGunakan dashboard ini untuk mengelola semua data barang, pengguna, dan laporan dengan mudah.\nPilih fitur yang ingin dijalankan:", title="Dashboard Karyawan"))
        console.print("""
[bold green]1.[/bold green] Edit Peminjam
[bold green]2.[/bold green] Hapus Peminjam
[bold green]3.[/bold green] Lihat Laporan Peminjam
[bold green]4.[/bold green] Cari
[bold green]5.[/bold green] Sorting
[bold green]6.[/bold green] Laporan Jumlah Peminjam
[bold green]7.[/bold green] Kembali                     
""")
        pilihan = input("Masukkan pilihan (1-7): ")
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
        elif pilihan == "7":
            pass
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")
def menu_laporan_employee():
   pass