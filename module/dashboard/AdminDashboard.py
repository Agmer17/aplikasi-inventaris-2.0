from rich.panel import Panel
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from module.Manager.UserManager import UserManager

from module.Manager.ItemsManager import ItemsManager

# testing





def main_menu(item_manager: ItemsManager, userManager:UserManager) -> None:
    console = Console()
    while True:
        console.clear()
        console.print(Panel.fit("👋 [bold cyan]Selamat datang, Admin![/bold cyan]\nGunakan dashboard ini untuk mengelola semua data barang, pengguna, dan laporan dengan mudah.\nPilih fitur yang ingin dijalankan:", title="Dashboard Admin"))
        console.print(""" 
[bold green]1.[/bold green] Barang 
[bold green]2.[/bold green] Kategori Barang 
[bold green]3.[/bold green] Karyawan 
[bold green]4.[/bold green] Supplier 
[bold green]5.[/bold green] Peminjam 
[bold green]6.[/bold green] Tambah Pengguna 
[bold green]7.[/bold green] Laporan 
[bold green]8.[/bold green] Keluar App
""")
        pilihan = input("Masukkan pilihan (1-8): ")

        if pilihan == "1":
            menu_barang(item_manager)  # Menambahkan item_manager sebagai argumen
        elif pilihan == "2":
            menu_kategori(item_manager)
        elif pilihan == "3":
            menu_karyawan(listDataUser=userManager)
        elif pilihan == "4":
            menu_supplier()
        elif pilihan == "5":
            menu_peminjam()
        elif pilihan == "6":
            menu_registrasi()
        elif pilihan == "7":
            menu_laporan()
        elif pilihan == "8":
            console.print("[bold red]Keluar dari aplikasi...[/bold red]")
            break
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")

def menu_barang(item_manager):
    console = Console()
    
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]Menu Barang[/bold cyan]"))
        console.print("""
1. Tambah Barang
2. Edit Barang
3. Hapus Barang
4. Lihat Daftar Barang
5. Cari Barang
6. Sorting Barang
7. Kelola Kategori Barang
8. Kembali
""")
        
        choice = input("Pilih opsi: ")

        if choice == '1':
            name = input("Masukkan nama barang: ")
            categories = item_manager.get_all_categories()
            print("Pilih kategori:")
            for category_id, category_name in categories.items():
                print(f"{category_id}. {category_name}")
            category_id = input("Masukkan ID kategori: ")
            category_name = categories.get(category_id, "Kategori tidak valid.")
            
            stock = int(input("Masukkan jumlah stok: "))
            price = int(input("Masukkan harga: "))
            sell_price = int(input("Masukkan harga jual: "))
            entrydate = datetime.now().isoformat()
            desc = input("Masukkan deskripsi barang: ")
            supplier = input("Masukkan supplier: ")
            status = input("Masukkan status (aktif/non-aktif): ")

            item_data = {
                "name": name,
                "category": category_name,
                "stock": stock,
                "price": price,
                "sellPrice": sell_price,
                "entrydate": entrydate,
                "desc": desc,
                "supplier": supplier,
                "status": status
            }

            item_manager.add_item(name, item_data)
            print("Barang berhasil ditambahkan.")

        elif choice == '2':
            items = item_manager.get_all_items()
            if items:
                table = Table(title="Daftar Barang untuk Edit")
                table.add_column("Nama Barang", style="cyan", justify="center")
                table.add_column("Kategori", style="magenta")
                table.add_column("Stok", style="green")
                
                for item_name, item in items.items():
                    table.add_row(item_name, item['category'], str(item['stock']))

                console.print(table)

                item_name = input("Masukkan nama barang yang ingin diedit: ")
                item = item_manager.get_item(item_name)
                if item:
                    print(f"Nama: {item['name']}, Kategori: {item['category']}, Stok: {item['stock']}")
                    category = input(f"Kategori ({item['category']}): ") or item['category']
                    stock = int(input(f"Stok ({item['stock']}): ") or item['stock'])
                    price = int(input(f"Harga ({item['price']}): ") or item['price'])
                    sell_price = int(input(f"Harga Jual ({item['sellPrice']}): ") or item['sellPrice'])
                    desc = input(f"Deskripsi ({item['desc']}): ") or item['desc']
                    supplier = input(f"Supplier ({item['supplier']}): ") or item['supplier']
                    status = input(f"Status ({item['status']}): ") or item['status']

                    updated_item = {
                        "name": item['name'],
                        "category": category,
                        "stock": stock,
                        "price": price,
                        "sellPrice": sell_price,
                        "entrydate": item['entrydate'],
                        "desc": desc,
                        "supplier": supplier,
                        "status": status
                    }

                    item_manager.update_item(item_name, updated_item)
                    print("Barang berhasil diperbarui.")
                else:
                    print("Barang tidak ditemukan.")
            else:
                print("Tidak ada barang untuk diedit.")

        elif choice == '3':
            items = item_manager.get_all_items()
            if items:
                table = Table(title="Daftar Barang untuk Hapus")
                table.add_column("Nama Barang", style="cyan", justify="center")
                table.add_column("Kategori", style="magenta")
                table.add_column("Stok", style="green")
                
                for item_name, item in items.items():
                    table.add_row(item_name, item['category'], str(item['stock']))

                console.print(table)

                item_name = input("Masukkan nama barang yang ingin dihapus: ")
                item_manager.delete_item(item_name)
                print("Barang berhasil dihapus.")
            else:
                print("Tidak ada barang untuk dihapus.")

        elif choice == '4':
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

        elif choice == '5':
            search_term = input("Masukkan nama barang yang ingin dicari: ")
            items = item_manager.search_item(search_term)
            if items:
                table = Table(title="Hasil Pencarian Barang")
                table.add_column("Nama Barang", style="cyan", justify="center")
                table.add_column("Kategori", style="magenta")
                table.add_column("Stok", style="green")

                for item_name, item in items.items():
                    table.add_row(item_name, item['category'], str(item['stock']))

                console.print(table)
            else:
                print("Barang tidak ditemukan.") 

        elif choice == '6':
            print("Sort By:")
            print("1. Nama")
            print("2. Harga")
            print("3. Stok")
            sort_choice = input("Pilih opsi untuk sorting: ")
            if sort_choice == '1':
                sorted_items = item_manager.sort_items('name')
            elif sort_choice == '2':
                sorted_items = item_manager.sort_items('price')
            elif sort_choice == '3':
                sorted_items = item_manager.sort_items('stock')
            else:
                print("Pilihan tidak valid.")
                continue

            if sorted_items:
                table = Table(title="Barang yang Disortir")
                table.add_column("Nama Barang", style="cyan", justify="center")
                table.add_column("Kategori", style="magenta")
                table.add_column("Stok", style="green")

                for item_name, item in sorted_items.items():
                    table.add_row(item_name, item['category'], str(item['stock']))

                console.print(table)
            else:
                print("Tidak ada barang.")

        elif choice == '7':
            menu_kategori(item_manager)

        elif choice == '8':
            break

        else:
            print("Pilihan tidak valid.")
            

def menu_kategori(item_manager):
    console = Console()
    
    while True:
        console.clear()
        console.print("[bold cyan]Menu Kategori Barang[/bold cyan]", style="bold underline")
        console.print("""
1. Lihat Daftar Kategori Barang
2. Tambah Kategori Barang
3. Edit Kategori Barang
4. Hapus Kategori Barang
5. Kembali
""")
        
        choice = input("Pilih opsi: ")

        if choice == '1':
            categories = item_manager.get_all_categories()
            if categories:
                table = Table(title="Daftar Kategori Barang untuk Edit")
                table.add_column("ID Kategori", style="cyan", justify="center")
                table.add_column("Nama Kategori", style="magenta")

                for category_id, category_name in categories.items():
                    table.add_row(category_id, category_name)

                console.print(table)
            else:
                console.print("[bold red]Tidak ada kategori.[/bold red]")

        elif choice == '2':
            category_name = input("Masukkan nama kategori baru: ")
            item_manager.add_category(category_name)
            console.print("[bold green]Kategori berhasil ditambahkan.[/bold green]")

        elif choice == '3':
            categories = item_manager.get_all_categories()
            if categories:
                table = Table(title="Daftar Kategori Barang untuk Edit")
                table.add_column("ID Kategori", style="cyan", justify="center")
                table.add_column("Nama Kategori", style="magenta")

                for category_id, category_name in categories.items():
                    table.add_row(category_id, category_name)

                console.print(table)

                category_id = input("Masukkan ID kategori yang ingin diedit: ")
                category_name = input("Masukkan nama kategori baru: ")
                item_manager.edit_category(category_id, category_name)
                console.print("[bold yellow]Kategori berhasil diperbarui.[/bold yellow]")
            else:
                console.print("[bold red]Tidak ada kategori yang bisa diedit.[/bold red]")

        elif choice == '4':
            categories = item_manager.get_all_categories()
            if categories:
                table = Table(title="Daftar Kategori Barang untuk Hapus")
                table.add_column("ID Kategori", style="cyan", justify="center")
                table.add_column("Nama Kategori", style="magenta")

                for category_id, category_name in categories.items():
                    table.add_row(category_id, category_name)

                console.print(table)

                category_id = input("Masukkan ID kategori yang ingin dihapus: ")
                item_manager.delete_category(category_id)
                console.print("[bold red]Kategori berhasil dihapus.[/bold red]")
            else:
                console.print("[bold red]Tidak ada kategori yang bisa dihapus.[/bold red]")

        elif choice == '5':
            break

        else:
            console.print("[bold red]Pilihan tidak valid.[/bold red]")

        
def menu_karyawan(listDataUser : UserManager):
    console = Console()
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]Menu Karyawan[/bold cyan]"))
        console.print("""
1. Edit Karyawan
2. Hapus Karyawan
3. Lihat Laporan Karyawan
4. Cari Barang
5. Sorting Barang 
6. Laporan Jumlah Karyawan
7. Kembali
""")
        choice = Prompt.ask("[chartreuse1]Pilih menu: [/chartreuse1]")
        match choice : 
            case "1" : 
                table = Table(title="User Information")
                table.add_column("Key", style="cyan")
                table.add_column("Name", style="green")
                table.add_column("Email", style="blue")
                table.add_column("Password", style="red")
                table.add_column("Role", style="magenta")

                # Add rows
                for user_key, user_info in listDataUser.items.items():
                    table.add_row(
                        user_key,
                        user_info.name,
                        user_info.email,
                        user_info.password,
                        user_info.role
                    )
                console.print(table)
                tempUsername = Prompt.ask("Masukan username yg ingin dirubah : ")
                
            case "7" : 
                break
            case _ : 
                break

def menu_supplier():
    console = Console()
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]Menu Supplier[/bold cyan]"))
        console.print("""
1. Edit Supplier
2. Hapus Supplier
3. Lihat Daftar Supplier
4. Cari Data Supplier
5. Sorting Data Supplier
6. Kembali
""")
        p = input("Pilih menu: ")
        if p == "6":
            break

def menu_peminjam():
    console = Console()
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]Menu Peminjam[/bold cyan]"))
        console.print("""
1. Edit Peminjam
2. Hapus Peminjam
3. Lihat Laporan Peminjam
4. Cari Data Peminjam
5. Sorting Data Peminjam
6. Kembali
""")
        p = input("Pilih menu: ")
        if p == "6":
            break

def menu_registrasi():
    console = Console()
    console.clear()
    console.print(Panel.fit("[bold cyan]Registrasi Pengguna[/bold cyan]"))
    console.print("👉 Fungsi ini mengambil dari User.py di folder manager")
    input("Tekan Enter untuk kembali...")

def menu_laporan():
    console = Console()
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]Menu Laporan[/bold cyan]"))
        console.print("""
1. Laporan Stok Barang
2. Laporan Transaksi Barang
3. Kembali
""")
        p = input("Pilih menu: ")
        if p == "3":
            break

# Eksekusi utama
if __name__ == "__main__":
    main_menu()
