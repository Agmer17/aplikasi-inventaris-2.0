from rich.panel import Panel
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from module.Manager.UserManager import UserManager
from module.Manager.ItemsManager import ItemsManager
import module.dashboard.Util as Util

# testing

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
        pilihan = input("Masukkan pilihan (1-8): ")

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
            # catgory table
            categoryTable = Table(title="Daftar Kategori")
            categoryTable.add_column("ID", style="cyan", justify="center")
            categoryTable.add_column("Nama Kategori", style="green")
            for category_id, category_name in item_manager.get_all_categories().items():
                categoryTable.add_row(str(category_id), category_name)
            # -----------------------
            
            
            # supplier table 
            supplierData = listDataUser.getDataByRole("supplier")
            supplierTable = Table(title="Daftar supplier")
            supplierTable.add_column("Username", style="cyan")
            supplierTable.add_column("Name", style="green")

            for username, user in supplierData.items():
                supplierTable.add_row(
                    username,
                    user.name,
                )

            # ---------------
            
            name = input("Masukkan nama barang: ")
            categories = item_manager.get_all_categories()
            
            # Menampilkan tabel
            console.print(categoryTable)
            
            
            category_id = input("Masukkan ID kategori: ")
            category_name = categories.get(category_id, "Kategori tidak valid.")
            
            stock = int(input("Masukkan jumlah stok: "))
            price = int(input("Masukkan harga: "))
            sell_price = int(input("Masukkan harga jual: "))
            entrydate = datetime.now().isoformat()
            desc = input("Masukkan deskripsi barang: ")
            console.print(supplierTable)
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
            Util.printTable("daftar karyawan", listDataUser, "employe")


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

                for key, prompt_text in fields.items():
                    new_value = Prompt.ask(prompt_text)
                    if new_value:
                        listDataUser.editUser(tempUsername, key, new_value)
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
                console.print("[yellow]Kosongkan input jika tidak ingin mengubah nilai tersebut[/yellow]")
                new_username = Prompt.ask("Username baru", default=username)
                new_name = Prompt.ask("Nama baru", default=supplier.name)
                new_email = Prompt.ask("Email baru", default=supplier.email)
                new_password = Prompt.ask("Password baru", default=supplier.password)

                if new_username != username:
                    # pindah data
                    user_data = listDataUser.items.pop(username)
                    user_data.changeUsername(new_username)
                    listDataUser.items[new_username] = user_data
                    username = new_username

                supplier = listDataUser.findUser(username)
                supplier.changeName(new_name)
                supplier.changeEmail(new_email)
                supplier.changePassword(new_password)

                console.print("[green]✅ Data supplier berhasil diubah[/green]")
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
                new_username = Prompt.ask("Username baru", default=username)
                new_name = Prompt.ask("Nama baru", default=peminjam.name)
                new_email = Prompt.ask("Email baru", default=peminjam.email)
                new_password = Prompt.ask("Password baru", default=peminjam.password)

                if new_username != username:
                    # Pindah data
                    user_data = listDataUser.items.pop(username)
                    user_data.changeUsername(new_username)
                    listDataUser.items[new_username] = user_data
                    username = new_username

                peminjam = listDataUser.findUser(username)
                peminjam.changeName(new_name)
                peminjam.changeEmail(new_email)
                peminjam.changePassword(new_password)

                console.print("[green]✅ Data peminjam berhasil diubah[/green]")
            else:
                console.print("[red]❌ Peminjam tidak ditemukan![/red]")
            input("Tekan Enter untuk lanjut...")

        elif p == "2":
            Util.printTable("daftar peminjam", listDataUser, "user")
            
            username = Prompt.ask("Masukkan username peminjam yang akan dihapus")
            user = listDataUser.findUser(username)
            if user and user.role == "pembeli":
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
1. Laporan Stok Barang
2. Laporan Transaksi Barang
3. Kembali
""")
        p = input("Pilih menu: ")
        if p == "3":
            break

# Eksekusi utama
if __name__ == "__main__":
    userManager = UserManager("path/ke/file_user.json")
    itemManager = ItemsManager("path/ke/barang.json")
    main_menu(itemManager, userManager)