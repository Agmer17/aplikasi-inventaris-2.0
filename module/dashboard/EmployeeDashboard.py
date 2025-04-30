# dashboard_employee.py
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from datetime import datetime
import json

itemsjsonfilepath = '../../data/items.json'


console = Console()
def tambah_barang_employee():
            # Kuisioner buat dibikin ke JSON
            name = input("Masukkan nama barang: ")
            # Default kalau jawaban kosong
            if not name:
                name = "Nama Belum Diisi"
            category = input("Masukkan kategori barang: ")
            # Default kalau jawaban kosong
            if not category:
                category = "-"
            stock = input("Masukkan jumlah stok barang(dalam angka): ").strip()
            # Default kalau jawaban kosong
            if not stock:
                stock = -1  # Nilai default
            else:
                stock = int(stock)
            price = input("Masukkan harga awal barang(dalam angka): ")
            # Default kalau jawaban kosong
            if not price:
                price = -1  # Nilai default
            else:
                price = int(price)
            sell_price = input("Masukkan harga jual barang(dalam angka): ")
            if not sell_price:
                sell_price = -1  # Nilai default
            else:
                sell_price = int(sell_price)
            entry_date = datetime.now().isoformat()
            description = input("Masukkan deskripsi barang: ")
            # Default kalau jawaban kosong
            if not description:
                description = "-"
            supplier = input("Masukkan nama supplier: ")
            # Default kalau jawaban kosong
            if not supplier:
                supplier= "-"
            status = input("Aktif/Tidak Aktif: ")
            # Default kalau jawaban kosong
            if not status:
                status= "Aktif"
            
            item_baru = {
            "name": name,
            "category": category,
            "stock": stock,
            "price": price,
            "sellPrice": sell_price,
            "entrydate": entry_date,
            "desc": description,
            "supplier": supplier,
            "status": status
            } 
            # Reading from a JSON file
            with open(itemsjsonfilepath, 'r') as file:
                data = json.load(file)

            # (append new object)
                data['items'][name] = item_baru

            # Writing back to the file
            with open(itemsjsonfilepath, 'w') as file:
                json.dump(data, file, indent=2)

def lihat_daftar_barang_employee():
    # Reading from a JSON file
    with open(itemsjsonfilepath, 'r') as file:
        data = json.load(file)
        table = Table(title="Daftar Barang")
        table.add_column("Nama", style="bold cyan")
        table.add_column("Kategori")
        table.add_column("Stok", justify="right")
        table.add_column("Harga Beli", justify="right")
        table.add_column("Harga Jual", justify="right")
        table.add_column("Tanggal Masuk")
        table.add_column("Deskripsi")
        table.add_column("Supplier")
        table.add_column("Status", style="green")
        for item_name, item in data["items"].items():
            table.add_row(
            item.get("name", "-"),
            item.get("category", "-"),
            str(item.get("stock", "-")),
            f"{item.get('price', 0):,}",
            f"{item.get('sellPrice', 0):,}",
            item.get("entrydate", "-"),
            item.get("desc", "-"),
            item.get("supplier", "-"),
            item.get("status", "-")
        )
            

        console.print(table)
        input()
            

def menu_utama_employee():
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
            tambah_barang_employee()
        elif pilihan == "2":
            pass
        elif pilihan == "3":
            lihat_daftar_barang_employee()
        elif pilihan == "4":
            pass
        elif pilihan == "5":
            pass
        elif pilihan == "6":
            # kembali ke menu utama
            return
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
            # kembali ke menu utama
            return
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
            # kembali ke menu utama
            return
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")
def menu_laporan_employee():
   pass


      
menu_utama_employee()