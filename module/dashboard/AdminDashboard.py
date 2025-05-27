from rich.panel import Panel
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from module.Manager.UserManager import UserManager
from module.Manager.ItemsManager import ItemsManager
import module.dashboard.Util as Util
from module.Manager.TransactionManager import TransactionManager

# testing
transaction = TransactionManager()

def main_menu(item_manager: ItemsManager, userManager:UserManager) -> None:
    console = Console()
    while True:
        console.clear()
        console.print(Panel.fit("👋 [bold cyan]Selamat datang, Admin![/bold cyan]\nGunakan dashboard ini untuk mengelola semua data barang, pengguna, dan laporan dengan mudah.\nPilih fitur yang ingin dijalankan:", title="Dashboard Admin"))
        console.print(""" 
[bold green]1.[/bold green] Barang 
[bold green]2.[/bold green] Karyawan 
[bold green]3.[/bold green] Supplier 
[bold green]4.[/bold green] Peminjam 
[bold green]5.[/bold green] Tambah Pengguna 
[bold green]6.[/bold green] Laporan 
[bold green]7.[/bold green] Keluar App
""")
        pilihan = input("Masukkan pilihan (1-7): ")

        if pilihan == "1":
            menu_barang(userManager,item_manager)  
        elif pilihan == "2":
            menu_karyawan(listDataUser=userManager)
        elif pilihan == "3":
            menu_supplier(listDataUser=userManager)
        elif pilihan == "4":
            menu_peminjam(listDataUser=userManager)
        elif pilihan == "5":
            menu_registrasi(userManager)
        elif pilihan == "6":
            menu_laporan()
        elif pilihan == "7":
            console.print("[bold red]Keluar dari aplikasi...[/bold red]")
            break
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")

def menu_barang(listDataUser:UserManager, item_manager:ItemsManager):
    
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
            
            # Menampilkan tabel
            Util.printTable("daftar items", item_manager, "categories")
            
            
            category_id = input("Masukkan ID kategori: ")
            category_name = categories.get(category_id, "Kategori tidak valid.")
            
            stock = int(input("Masukkan jumlah stok: "))
            price = int(input("Masukkan harga: "))
            sell_price = int(input("Masukkan harga jual: "))
            entrydate = datetime.now().isoformat()
            desc = input("Masukkan deskripsi barang: ")
            Util.printTable("daftar supplier", listDataUser, "supplier")
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
            Util.createTransaction(name, 0, stock, supplier, price, transaction, "Penambahan barang baru")
            print("Barang berhasil ditambahkan.")

        elif choice == '2':
            Util.printTable("daftar item", item_manager, "items")
            item_name = Prompt.ask("Masukkan nama barang yang ingin diedit: ")
            item = item_manager.get_item(item_name)

            if item:
                stok_awal = int(item['stock'])
                
                fields = {
                    "name": f"Nama [{item['name']}]",
                    "category": f"Kategori [{item['category']}]",
                    "stock": f"Stok [{item['stock']}]",
                    "price": f"Harga [{item['price']}]",
                    "sellPrice": f"Harga Jual [{item['sellPrice']}]",
                    "desc": f"Deskripsi [{item['desc']}]",
                    "supplier": f"Supplier [{item['supplier']}]",
                    "status": f"Status [{item['status']}]"
                }
                updated_item:dict = Util.editAllData(item_name, item_manager, fields)
                console.print("[bold green]Barang berhasil diperbarui.[/bold green]")
                input()

                # Cek perubahan stok
                stok_baru = int(updated_item["stock"])
                input(f"{stok_baru}")
                selisih = stok_baru - stok_awal

                if selisih != 0:
                    Util.createTransaction(updated_item["name"], stok_awal, stok_baru, updated_item["supplier"], updated_item["price"], transaction)

            else:
                console.print("[bold red]Barang tidak ditemukan.[/bold red]")
                Prompt.ask("[bold yellow] tekan enter untuk kembali[/bold yellow]")


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
            Util.printTable("daftar items", item_manager, "items")
            Prompt.ask("[bold yellow] tekan enter untuk lanjut[/bold yellow]")

        elif choice == '5':
            search_term = Prompt.ask("[bold cyan]Masukkan nama barang yang ingin dicari[/bold cyan]")
            items = item_manager.search_item(search_term)
            if items:
                table = Table(title="Hasil Pencarian Barang")
                table.add_column("Nama Barang", style="cyan", justify="center")
                table.add_column("Kategori", style="magenta")
                table.add_column("Stok", style="green", justify="right")

                for item_name, item in items.items():
                    table.add_row(item_name, item['category'], str(item['stock']))

                console.print(table)
                Prompt.ask("[bold yellow]Tekan enter untuk lanjut[/bold yellow]")
            else:
                console.print("[bold red]Barang tidak ditemukan.[/bold red]")
                Prompt.ask("[bold yellow]Tekan enter untuk kembali[/bold yellow]")

        elif choice == '6':
            console.print("[bold cyan]Sort By:[/bold cyan]")
            console.print("1. Nama\n2. Harga\n3. Stok")
            sort_choice = Prompt.ask("Pilih opsi untuk sorting", choices=["1", "2", "3"], default="1")

            if sort_choice == '1':
                sorted_items = item_manager.get_sorted_items(by="name")
            elif sort_choice == '2':
                sorted_items = item_manager.get_sorted_items(by="price")
            elif sort_choice == '3':
                sorted_items = item_manager.get_sorted_items(by="stock")

            if sorted_items:
                table = Table(title="Barang yang Disortir")
                table.add_column("Nama Barang", style="cyan", justify="center")
                table.add_column("Kategori", style="magenta")
                table.add_column("Stok", style="green", justify="right")

                for item_name, item in sorted_items:
                    table.add_row(item_name, item["category"], str(item["stock"]))

                console.print(table)
            else:
                console.print("[bold red]Tidak ada barang.[/bold red]")

            Prompt.ask("[bold yellow]Tekan enter untuk kembali[/bold yellow]")

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
            Util.printTable("daftar items", item_manager, "categories")
            Prompt.ask("[bold yellow] tekan enter untuk lanjut[/bold yellow]")

        elif choice == '2':
            category_name = input("Masukkan nama kategori baru: ")
            item_manager.add_category(category_name)
            console.print("[bold green]Kategori berhasil ditambahkan.[/bold green]")
            Prompt.ask("[bold yellow] tekan enter untuk lanjut[/bold yellow]")

        elif choice == '3':
            Util.printTable("daftar items", item_manager, "categories")

            category_id = input("Masukkan ID kategori yang ingin diedit: ")
            category_name = input("Masukkan nama kategori baru: ")
            item_manager.edit_category(category_id, category_name)
            console.print("[bold yellow]Kategori berhasil diperbarui.[/bold yellow]")
            Prompt.ask("[bold yellow] tekan enter untuk lanjut[/bold yellow]")


        elif choice == '4':
            Util.printTable("daftar items", item_manager, "categories")

            category_id = input("Masukkan ID kategori yang ingin dihapus: ")
            item_manager.delete_category(category_id)
            console.print("[bold red]Kategori berhasil dihapus.[/bold red]")
            Prompt.ask("[bold yellow] tekan enter untuk lanjut[/bold yellow]")
            
        elif choice == '5':
            break

        else:
            console.print("[bold red]Pilihan tidak valid.[/bold red]")

        
def menu_karyawan(listDataUser: UserManager):
    console = Console()
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]Menu Karyawan[/bold cyan]"))
        console.print("""
1. Edit Karyawan
2. Hapus Karyawan
3. Lihat daftar Karyawan
4. Kembali
""")
        choice = Prompt.ask("[chartreuse1]Pilih menu: [/chartreuse1]")

        if choice == "1":
            Util.printTable("daftar karyawan", listDataUser, "employee")


            tempUsername = Prompt.ask("Masukkan username yang ingin diedit: ")
            user = listDataUser.findUser(tempUsername)

            if user and user.role == "employee":
                console.print("[yellow]Kosongkan input jika tidak ingin mengubah field tersebut.[/yellow]")

                fields = {
                    "username": f"Username baru [{user.username}]",
                    "nama": f"Nama baru [{user.name}]",
                    "email": f"Email baru [{user.email}]",
                    "password": f"Password baru [{user.password}]"
                }

                Util.editAllData(tempUsername, listDataUser, fields)
                console.print("[green]✅ Data karyawan berhasil diperbarui.[/green]")
            else:
                console.print("[red]Username tidak ditemukan atau bukan karyawan![/red]")

            input("Tekan ENTER untuk lanjut...")

        elif choice == "2":
            # Tampilkan semua employee
            Util.printTable("daftar karyawan", listDataUser, "employee")
            
            tempUsername = Prompt.ask("Masukkan username yang ingin dihapus: ")
            user = listDataUser.findUser(tempUsername)
            if user and user.role == "employee":
                listDataUser.deleteData(tempUsername)
                console.print("[green]Data karyawan berhasil dihapus.[/green]")
            else:
                console.print("[red]Username tidak ditemukan atau bukan karyawan![/red]")
            input("Tekan ENTER untuk lanjut...")

        elif choice == "3":
            Util.printTable("daftar karyawan", listDataUser, "employee")
            input("Tekan ENTER untuk lanjut...")

        elif choice == "4":
            break

        else:
            console.print("[red]Pilihan tidak valid![/red]")
            input("Tekan ENTER untuk lanjut...")

def menu_supplier(listDataUser: UserManager):
    console = Console()
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]Menu Supplier[/bold cyan]"))
        console.print("""
[bold yellow]1.[/bold yellow] Edit Supplier
[bold yellow]2.[/bold yellow] Hapus Supplier
[bold yellow]3.[/bold yellow] Lihat Daftar Supplier
[bold yellow]4.[/bold yellow] Cari Data Supplier
[bold yellow]5.[/bold yellow] Sorting Data Supplier
[bold yellow]6.[/bold yellow] Kembali
""")

        p = Prompt.ask("[green]Pilih menu[/green]")

        if p == "1":
            Util.printTable("daftar supplier", listDataUser, "supplier")
            
            username = Prompt.ask("Masukkan username supplier yang ingin diedit")
            supplier = listDataUser.findUser(username)
            if supplier and supplier.role == "supplier":
                console.print("[yellow]Kosongkan input jika tidak ingin mengubah field tersebut.[/yellow]")

                fields = {
                    "username": f"Username baru [{supplier.username}]",
                    "nama": f"Nama baru [{supplier.name}]",
                    "email": f"Email baru [{supplier.email}]",
                    "password": f"Password baru [{supplier.password}]"
                }

                Util.editAllData(username, listDataUser, fields)
                console.print("[green]✅ Data karyawan berhasil diperbarui.[/green]")
            else:
                console.print("[red]❌ Supplier tidak ditemukan![/red]")
            input("Tekan Enter untuk lanjut...")

        elif p == "2":
            Util.printTable("daftar supplier", listDataUser, "supplier")
            
            username = Prompt.ask("Masukkan username supplier yang akan dihapus")
            user = listDataUser.findUser(username)
            if user and user.role == "supplier":
                listDataUser.deleteData(username)
                console.print("[green]Supplier berhasil dihapus.[/green]")
            else:
                console.print("[red]❌ Supplier tidak ditemukan![/red]")
            input("Tekan Enter untuk lanjut...")

        elif p == "3":
            Util.printTable("daftar supplier", listDataUser, "supplier")
            input("Tekan Enter untuk lanjut...")

        elif p == "4":
            Util.printTable("daftar supplier", listDataUser, "supplier")
            
            username = Prompt.ask("Masukkan username supplier")
            user = listDataUser.findUser(username)
            if user and user.role == "supplier":
                console.print(f"[cyan]Username:[/cyan] {user.username}")
                console.print(f"[green]Nama:[/green] {user.name}")
                console.print(f"[blue]Email:[/blue] {user.email}")
                console.print(f"[magenta]Role:[/magenta] {user.role}")
            else:
                console.print("[red]Supplier tidak ditemukan![/red]")
            input("Tekan Enter untuk lanjut...")

        elif p == "5":
            suppliers = listDataUser.getDataByRole("supplier")
            sorted_data = dict(sorted(suppliers.items()))
            table = Table(title="Supplier Tersorting")
            table.add_column("Username", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Email", style="blue")
            for username, user in sorted_data.items():
                table.add_row(username, user.name, user.email)
            console.print(table)
            input("Tekan Enter untuk lanjut...")

        elif p == "6":
            break

        else:
            console.print("[red]Pilihan tidak valid![/red]")
            input("Tekan Enter untuk lanjut...")
            
def menu_peminjam(listDataUser: UserManager):
    console = Console()
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]Menu Peminjam[/bold cyan]"))
        console.print("""
1. Edit Peminjam
2. Hapus Peminjam
3. Lihat Daftar Peminjam
4. Cari Data Peminjam
5. Sorting Data Peminjam
6. Kembali
""")
        p = Prompt.ask("[chartreuse1]Pilih menu: [/chartreuse1]")

        if p == "1":
            Util.printTable("daftar peminjam", listDataUser, "user")
            
            username = Prompt.ask("Masukkan username peminjam yang ingin diedit")
            peminjam = listDataUser.findUser(username)
            if peminjam and peminjam.role == "user":
                console.print("[yellow]Kosongkan input jika tidak ingin mengubah nilai tersebut[/yellow]")
                fields = {
                    "username": f"Username baru [{user.username}]",
                    "nama": f"Nama baru [{user.name}]",
                    "email": f"Email baru [{user.email}]",
                    "password": f"Password baru [{user.password}]"
                }
                
                Util.editAllData(username, listDataUser, fields)

                console.print("[green]✅ Data peminjam berhasil diubah[/green]")
            else:
                console.print("[red]❌ Peminjam tidak ditemukan![/red]")
            input("Tekan Enter untuk lanjut...")

        elif p == "2":
            Util.printTable("daftar peminjam", listDataUser, "user")
            
            username = Prompt.ask("Masukkan username peminjam yang akan dihapus")
            user = listDataUser.findUser(username)
            if user and user.role == "user":
                listDataUser.deleteData(username)
                console.print("[green]Peminjam berhasil dihapus.[/green]")
            else:
                console.print("[red]❌ Peminjam tidak ditemukan![/red]")
            input("Tekan Enter untuk lanjut...")

        elif p == "3":
            Util.printTable("daftar peminjam", listDataUser, "user")
            input("Tekan Enter untuk lanjut...")

        elif p == "4":
            Util.printTable("daftar peminjam", listDataUser, "user")
            
            username = Prompt.ask("Masukkan username peminjam")
            user = listDataUser.findUser(username)
            if user and user.role == "user":
                console.print(f"[cyan]Username:[/cyan] {user.username}")
                console.print(f"[green]Nama:[/green] {user.name}")
                console.print(f"[blue]Email:[/blue] {user.email}")
                console.print(f"[magenta]Role:[/magenta] {user.role}")
            else:
                console.print("[red]Peminjam tidak ditemukan![/red]")
            input("Tekan Enter untuk lanjut...")

        elif p == "5":
            peminjam = listDataUser.getDataByRole("user")
            sorted_data = dict(sorted(peminjam.items()))
            table = Table(title="Peminjam Tersorting")
            table.add_column("Username", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Email", style="blue")
            for username, user in sorted_data.items():
                table.add_row(username, user.name, user.email)
            console.print(table)
            input("Tekan Enter untuk lanjut...")

        elif p == "6":
            break

        else:
            console.print("[red]Pilihan tidak valid![/red]")
            input("Tekan Enter untuk lanjut...")
        
def menu_registrasi(userManager: UserManager):
    console = Console()
    console.clear()
    console.print(Panel.fit("[bold cyan]Registrasi Pengguna[/bold cyan]"))
    
    name = Prompt.ask("Masukkan nama")
    username = Prompt.ask("Masukkan username")
    email = Prompt.ask("Masukkan email")
    password = Prompt.ask("Masukkan password")
    role = Prompt.ask("Masukkan role (admin/employee/supplier/pembeli)", choices=["admin", "employee", "supplier", "pembeli"])

    # ubah pembeli menjadi user
    if role == "pembeli":
        role = "user"

    data = {
        "name": name,
        "username": username,
        "email": email,
        "password": password,
        "role": role
    }

    berhasil = userManager.addData(data)
    if berhasil:
        console.print("[green]✅ Pengguna berhasil ditambahkan![/green]")
    else:
        console.print("[red]❌ Gagal menambahkan pengguna. Username mungkin sudah digunakan atau role tidak valid.[/red]")

    input("Tekan Enter untuk kembali...")
    
    

def menu_laporan():
    console = Console()
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]Menu Laporan[/bold cyan]"))
        console.print("""
1. Lihat Transaksi
2. Buat Laporan Trasanksi Barang
3. Kembali
""")
        p = input("Pilih menu: ")
        if p == "1" :
            Util.display_transactions(transaction)
            input()
        elif p == "2" :
            Util.generate_transaction_report_rich(transaction)
            input()
        elif p == "3":
            break

# Eksekusi utama
if __name__ == "__main__":
    userManager = UserManager("path/ke/file_user.json")
    itemManager = ItemsManager("path/ke/barang.json")
    main_menu(itemManager, userManager)