# dashboard_employee.py
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from datetime import datetime
import json

itemsjsonfilepath = '../../data/items.json'
userjsonfilepath = '../../data/user.json'

console = Console()
# Fitur Dari Dashboard
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
        # membuat tabel 
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
            
def search_barang_employee():
    found = False
    input_name = input("Masukkan nama barang yang ingin anda cari: ").lower()
    input_category = input("Masukkan kategori barang yang ingin anda cari: ").lower()
    table = Table(title="Hasil Pencarian Barang")
    table.add_column("Nama", style="cyan", no_wrap=True)
    table.add_column("Kategori", style="magenta")
    with open(itemsjsonfilepath, 'r') as file:
        data = json.load(file)
        dataitem = data['items']
    #
    for key, value in dataitem.items():
        current_name = key.lower()
        current_category = value['category'].lower()
        if(not input_name or current_name.startswith(input_name) and (not input_category or current_category.startswith(input_category))):
            found = True
            table.add_row(current_name, current_category)
    if found:
        console.print(table)
        input()
    else:
        console.print("[red]Tidak ada item yang cocok.[/red]")
        input()

def sorting_barang_employee():
    # Baca data dari file JSON
    with open(itemsjsonfilepath, "r") as f:
        data = json.load(f)

    # Sort berdasarkan nama item (key dari "items")
    sorted_items = dict(sorted(data["items"].items(), key=lambda x: x[0].lower()))

    # Buat tabel
    table = Table(title="Daftar Barang (Urut Abjad)")

    # Tambahkan kolom
    table.add_column("Nama")
    table.add_column("Kategori")
    table.add_column("Stok", justify="right")
    table.add_column("Harga Beli", justify="right")
    table.add_column("Harga Jual", justify="right")
    table.add_column("Tanggal Masuk")
    table.add_column("Deskripsi")
    table.add_column("Supplier")
    table.add_column("Status")

    # Isi baris tabel
    for name, item in sorted_items.items():
        table.add_row(
            name,
            item.get("category", "-"),
            str(item.get("stock", "-")),
            f"Rp{item.get('price', 0):,}",
            f"Rp{item.get('sellPrice', 0):,}",
            item.get("entrydate", "-"),
            item.get("desc", "-"),
            item.get("supplier", "-"),
            item.get("status", "-")
        )

    # Tampilkan tabel
    console = Console()
    console.print(table)
    input()

def edit_supplier_peminjam(angka):
    #Supplier
    if angka == 2:
        pass
    #Peminjam
    elif angka == 3:
        pass
def hapus_supplier_peminjam(angka):
    with open(userjsonfilepath, "r") as f:
        datauser = json.load(f)
    #Supplier
    if angka == 2:
            # Inisialisasi tabel
            table = Table(title="Daftar Pengguna Role: Supplier")
            # Tambahkan kolom
            table.add_column("Username", style="cyan", no_wrap=True)
            table.add_column("Nama", style="green")
            table.add_column("Email", style="magenta")
            table.add_column("Role", style="yellow")
            table.add_column("Password", style="red")
            # Filter dan tambahkan baris hanya yang role-nya supplier
            for username, info in datauser.items():
                if info.get("role") == "supplier":
                    table.add_row(
                        username,
                        info.get("name", "-"),
                        info.get("email", "-"),
                        info.get("role", "-"),
                        info.get("password", "-")
                    )
            # Tampilkan tabel
            console = Console()
            console.print(table)
            input()
            pilihanhapus = input("Pilih Username yang ingin anda hapus: ").strip()
            if pilihanhapus in datauser:
                del datauser[pilihanhapus]
                print(f"Pengguna '{pilihanhapus}' berhasil dihapus.")

                # Simpan perubahan
                with open(userjsonfilepath, "w") as f:
                    json.dump(datauser, f, indent=4)
            else:
                print(f"Username '{pilihanhapus}' tidak ditemukan.")

    #Peminjam
    elif angka == 3:
            # Inisialisasi tabel
            table = Table(title="Daftar Pengguna Role: Peminjam")
            # Tambahkan kolom
            table.add_column("Username", style="cyan", no_wrap=True)
            table.add_column("Nama", style="green")
            table.add_column("Email", style="magenta")
            table.add_column("Role", style="yellow")
            table.add_column("Password", style="red")
            # Filter dan tambahkan baris hanya yang role-nya supplier
            for username, info in datauser.items():
                if info.get("role") == "peminjam":
                    table.add_row(
                        username,
                        info.get("name", "-"),
                        info.get("email", "-"),
                        info.get("role", "-"),
                        info.get("password", "-")
                    )
            # Tampilkan tabel
            console = Console()
            console.print(table)
            input()
            pilihanhapus = input("Pilih Username yang ingin anda hapus: ").strip()
            if pilihanhapus in datauser:
                del datauser[pilihanhapus]
                print(f"Pengguna '{pilihanhapus}' berhasil dihapus.")

                # Simpan perubahan
                with open(userjsonfilepath, "w") as f:
                    json.dump(datauser, f, indent=4)
            else:
                print(f"Username '{pilihanhapus}' tidak ditemukan.")
def lihat_daftar_supplier_peminjam(angka):
    with open(userjsonfilepath, "r") as f:
        datauser = json.load(f)
    #Supplier
    if angka == 2:
        # Inisialisasi tabel
        table = Table(title="Daftar Pengguna Role: Supplier")
        # Tambahkan kolom
        table.add_column("Username", style="cyan", no_wrap=True)
        table.add_column("Nama", style="green")
        table.add_column("Email", style="magenta")
        table.add_column("Role", style="yellow")
        table.add_column("Password", style="red")
        # Filter dan tambahkan baris hanya yang role-nya supplier
        for username, info in datauser.items():
            if info.get("role") == "supplier":
                table.add_row(
                    username,
                    info.get("name", "-"),
                    info.get("email", "-"),
                    info.get("role", "-"),
                    info.get("password", "-")
                )
        # Tampilkan tabel
        console = Console()
        console.print(table)
        input()
    #Peminjam
    elif angka == 3:
        # Inisialisasi tabel
        table = Table(title="Daftar Pengguna Role: Peminjam")
        # Tambahkan kolom
        table.add_column("Username", style="cyan", no_wrap=True)
        table.add_column("Nama", style="green")
        table.add_column("Email", style="magenta")
        table.add_column("Role", style="yellow")
        table.add_column("Password", style="red")
        # Filter dan tambahkan baris hanya yang role-nya supplier
        for username, info in datauser.items():
            if info.get("role") == "peminjam":
                table.add_row(
                    username,
                    info.get("name", "-"),
                    info.get("email", "-"),
                    info.get("role", "-"),
                    info.get("password", "-")
                    )
        # Tampilkan tabel
        console = Console()
        console.print(table)
        input()
def cari_supplier_peminjam(angka):
    #Supplier
    if angka == 2:
        pass
    #Peminjam
    elif angka == 3:
        pass
def sorting_supplier_peminjam(angka):
    #Supplier
    if angka == 2:
        pass
    #Peminjam
    elif angka == 3:
        pass

# Nenu Dashboard
def menu_utama_employee():
    while True:
        console.clear()
        console.print(Panel.fit("👋 [bold cyan]Selamat datang, Karyawan![/bold cyan]\nGunakan dashboard ini untuk mengelola semua data barang, supplier, peminjam, dan laporan dengan mudah.\nPilih fitur yang ingin dijalankan:", title="Dashboard Karyawan"))
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
            menu_supplierdanPeminjam_employee(2)
        elif pilihan == "3":
            menu_supplierdanPeminjam_employee(3)
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
        console.print(Panel.fit("👋 [bold cyan]Selamat datang, Karyawan![/bold cyan]\nGunakan dashboard ini untuk mengelola semua data barang dengan mudah.\nPilih fitur yang ingin dijalankan:", title="Dashboard Barang Karyawan"))
        console.print("""
[bold green]1.[/bold green] Tambah Barang
[bold green]2.[/bold green] Lihat Daftar Barang
[bold green]3.[/bold green] Cari
[bold green]4.[/bold green] Sorting
[bold green]5.[/bold green] Kembali                     
""")
        pilihan = input("Masukkan pilihan (1-6): ")
        if pilihan == "1":
            tambah_barang_employee()
        elif pilihan == "2":
            lihat_daftar_barang_employee()
        elif pilihan == "3":
            search_barang_employee()
        elif pilihan == "4":
            sorting_barang_employee()
        elif pilihan == "5":
            # kembali ke menu utama
            return
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")
def menu_supplierdanPeminjam_employee(angka):
    # Ini buat supplier
    if angka == 2:
        while True:
            console.clear()
            console.print(Panel.fit("👋 [bold cyan]Selamat datang, Karyawan![/bold cyan]\nGunakan dashboard ini untuk mengelola semua data Supplier dengan mudah.\nPilih fitur yang ingin dijalankan:", title="Dashboard Supplier Karyawan"))
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
                edit_supplier_peminjam(2)
            elif pilihan == "2":
                hapus_supplier_peminjam(2)
            elif pilihan == "3":
                lihat_daftar_supplier_peminjam(2)
            elif pilihan == "4":
                cari_supplier_peminjam(2)
            elif pilihan == "5":
                sorting_supplier_peminjam(2)
            elif pilihan == "6":
                # kembali ke menu utama
                return
            else:
                console.print("[bold red]Pilihan tidak valid![/bold red]")
    # Ini buat peminjam
    if angka == 3:
        while True:
            console.clear()
            console.print(Panel.fit("👋 [bold cyan]Selamat datang, Karyawan![/bold cyan]\nGunakan dashboard ini untuk mengelola semua data Peminjam dengan mudah.\nPilih fitur yang ingin dijalankan:", title="Dashboard Peminjam Karyawan"))
            console.print("""
    [bold green]1.[/bold green] Edit Peminjam
    [bold green]2.[/bold green] Hapus Peminjam
    [bold green]3.[/bold green] Lihat Daftar Peminjam
    [bold green]4.[/bold green] Cari
    [bold green]5.[/bold green] Sorting
    [bold green]6.[/bold green] Kembali                     
    """)
            pilihan = input("Masukkan pilihan (1-6): ")
            if pilihan == "1":
                edit_supplier_peminjam(3)
            elif pilihan == "2":
                hapus_supplier_peminjam(3)
            elif pilihan == "3":
                lihat_daftar_supplier_peminjam(3)
            elif pilihan == "4":
                cari_supplier_peminjam(3)
            elif pilihan == "5":
                sorting_supplier_peminjam(3)
            elif pilihan == "6":
                # kembali ke menu utama
                return
            else:
                console.print("[bold red]Pilihan tidak valid![/bold red]")

def menu_laporan_employee():
   pass



menu_utama_employee()