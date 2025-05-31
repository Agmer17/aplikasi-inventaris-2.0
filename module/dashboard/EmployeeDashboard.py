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
transaction = TransactionManager();

def validate_input(prompt_text, allow_empty=False, input_type="string"):
    """
    Fungsi untuk memvalidasi input dari pengguna
    """
    while True:
        user_input = input(prompt_text).strip()
        
        if not allow_empty and not user_input:
            print("[bold red]❌ Input tidak boleh kosong![/bold red]")
            continue
            
        if input_type == "int":
            try:
                return int(user_input)
            except ValueError:
                print("[bold red]❌ Input harus berupa angka![/bold red]")
                continue
        
        return user_input

def main_menu(item_manager: ItemsManager, userManager:UserManager) -> None:
    
    console = Console()
    while True:
        console.clear()
        console.print(Panel.fit("👋 [bold cyan]Selamat datang, karyawan![/bold cyan]\nGunakan dashboard ini untuk mengelola semua data barang, pengguna, dan laporan dengan mudah.\nPilih fitur yang ingin dijalankan:", title="Dashboard Admin"))
        console.print(""" 
[bold green]1.[/bold green] Barang 
[bold green]2.[/bold green] Supplier 
[bold green]3.[/bold green] Peminjam 
[bold green]4.[/bold green] Laporan 
[bold green]5.[/bold green] Keluar App
""")
        pilihan = input("Masukkan pilihan (1-5): ")
        if pilihan == "1":
            menu_barang(userManager,item_manager)  
        elif pilihan == "2":
            menu_supplier(listDataUser=userManager)
        elif pilihan == "3":
            menu_pembeli(listDataUser=userManager)
        elif pilihan == "4":
            menu_laporan()
        elif pilihan == "5":
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
            console.print("[bold yellow]⚠️ Semua field wajib diisi![/bold yellow]")
            
            name = validate_input("Masukkan nama barang: ")
            categories = item_manager.get_all_categories()
            
            if not categories:
                console.print("[bold red]❌ Tidak ada kategori tersedia. Tambahkan kategori terlebih dahulu![/bold red]")
                input("Tekan Enter untuk kembali...")
                continue
            
            Util.printTable("daftar items", item_manager, "categories")
            
            category_id = validate_input("Masukkan ID kategori: ")
            category_name = categories.get(category_id)
            
            if not category_name:
                console.print("[bold red]❌ ID kategori tidak valid![/bold red]")
                input("Tekan Enter untuk kembali...")
                continue
            
            stock = validate_input("Masukkan jumlah stok: ", input_type="int")
            price = validate_input("Masukkan harga: ", input_type="int")
            sell_price = validate_input("Masukkan harga jual: ", input_type="int")
            entrydate = datetime.now().isoformat()
            desc = validate_input("Masukkan deskripsi barang: ")
            
            suppliers = listDataUser.getDataByRole("supplier")
            if not suppliers:
                console.print("[bold red]❌ Tidak ada supplier tersedia. Tambahkan supplier terlebih dahulu![/bold red]")
                input("Tekan Enter untuk kembali...")
                continue
                
            Util.printTable("daftar supplier", listDataUser, "supplier")
            supplier = validate_input("Masukkan username supplier: ")
            
            supplier_user = listDataUser.findUser(supplier)
            if not supplier_user or supplier_user.role != "supplier":
                console.print("[bold red]❌ Supplier tidak ditemukan![/bold red]")
                input("Tekan Enter untuk kembali...")
                continue
            
            while True:
                status = validate_input("Masukkan status (aktif/non-aktif): ").lower()
                if status in ["aktif", "non-aktif"]:
                    break
                console.print("[bold red]❌ Status harus 'aktif' atau 'non-aktif'![/bold red]")

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
            console.print(f"[green]✅ Barang '{name}' berhasil ditambahkan.[/green]")
            input("Tekan Enter untuk lanjut...")

        elif choice == '2':
            items = item_manager.get_all_items()
            if not items:
                console.print("[bold red]❌ Tidak ada barang untuk diedit![/bold red]")
                input("Tekan Enter untuk kembali...")
                continue
                
            Util.printTable("daftar item", item_manager, "items")
            
            while True:
                item_name = input("Masukkan nama barang yang ingin diedit: ").strip()
                if not item_name:
                    console.print("[bold red]❌ Nama barang tidak boleh kosong![/bold red]")
                    continue
                break
            
            item = None
            original_item_name = None
            
            if item_name in items:
                item = items[item_name]
                original_item_name = item_name
            else:
                for key, value in items.items():
                    if key.lower() == item_name.lower():
                        item = value
                        original_item_name = key
                        break

            if item:
                stok_awal = int(item['stock'])
                
                console.print(f"[bold green]✅ Ditemukan barang: {original_item_name}[/bold green]")
                console.print("[yellow]⚠️ Kosongkan input jika tidak ingin mengubah field tersebut.[/yellow]")
                console.print("[bold cyan]💡 Nama barang tidak boleh kosong![/bold cyan]")
                
                while True:
                    new_name = input(f"Nama [{item['name']}]: ").strip()
                    if new_name == "":
                        new_name = item['name']
                        break
                    elif new_name:
                        break
                    else:
                        console.print("[bold red]❌ Nama barang tidak boleh kosong![/bold red]")
                        continue
                
                fields = {
                    "name": new_name,
                    "category": input(f"Kategori [{item['category']}]: ").strip() or item['category'],
                    "stock": input(f"Stok [{item['stock']}]: ").strip() or item['stock'],
                    "price": input(f"Harga [{item['price']}]: ").strip() or item['price'],
                    "sellPrice": input(f"Harga Jual [{item['sellPrice']}]: ").strip() or item['sellPrice'],
                    "desc": input(f"Deskripsi [{item['desc']}]: ").strip() or item['desc'],
                    "supplier": input(f"Supplier [{item['supplier']}]: ").strip() or item['supplier'],
                    "status": input(f"Status [{item['status']}]: ").strip() or item['status']
                }
                
                try:
                    fields["stock"] = int(fields["stock"]) if str(fields["stock"]).isdigit() else int(item['stock'])
                    fields["price"] = float(fields["price"]) if str(fields["price"]).replace('.', '').isdigit() else float(item['price'])
                    fields["sellPrice"] = float(fields["sellPrice"]) if str(fields["sellPrice"]).replace('.', '').isdigit() else float(item['sellPrice'])
                except ValueError:
                    console.print("[bold red]❌ Format angka tidak valid, menggunakan nilai lama.[/bold red]")
                    fields["stock"] = int(item['stock'])
                    fields["price"] = float(item['price'])
                    fields["sellPrice"] = float(item['sellPrice'])
                
                updated_item = item_manager.update_item(original_item_name, fields)
                console.print("[bold green]✅ Barang berhasil diperbarui.[/bold green]")

                stok_baru = int(fields["stock"])
                selisih = stok_baru - stok_awal

                if selisih != 0:
                    Util.createTransaction(fields["name"], stok_awal, stok_baru, fields["supplier"], fields["price"], transaction)

            else:
                console.print(f"[bold red]❌ Barang '{item_name}' tidak ditemukan.[/bold red]")
                
            input("Tekan Enter untuk kembali...")

        elif choice == '3':
            items = item_manager.get_all_items()
            if items:
                table = Table(title="Daftar Barang untuk Dihapus")
                table.add_column("Nama Barang", style="cyan", justify="center")
                table.add_column("Kategori", style="magenta")
                table.add_column("Stok", style="green")

                for item_name, item in items.items():
                    table.add_row(item_name, item['category'], str(item['stock']))

                console.print(table)

                input_name = validate_input("Masukkan nama barang yang ingin dihapus: ").strip().lower()

                matched_item_name = None
                for item_name in items:
                    if item_name.lower() == input_name:
                        matched_item_name = item_name
                        break

                if matched_item_name:
                    while True:
                        confirm = input(f"Apakah Anda yakin ingin menghapus '{matched_item_name}'? (y/n): ").strip().lower()
                        if confirm in ['y', 'n']:
                            break
                        console.print("[bold red]❌ Input harus 'y' atau 'n'![/bold red]")
                    
                    if confirm == 'y':
                        item_manager.delete_item(matched_item_name)
                        console.print(f"[green]✅ Barang '{matched_item_name}' berhasil dihapus.[/green]")
                    else:
                        console.print("[yellow]⚠️ Penghapusan dibatalkan.[/yellow]")
                else:
                    console.print(f"[red]❌ Barang dengan nama '{input_name}' tidak ditemukan.[/red]")
            else:
                console.print("[yellow]⚠️ Tidak ada barang untuk dihapus.[/yellow]")
            input("Tekan Enter untuk kembali...")

        elif choice == '4':
            Util.printTable("daftar items", item_manager, "items")
            input("Tekan Enter untuk lanjut...")

        elif choice == '5':
            search_term = validate_input("Masukkan nama barang yang ingin dicari: ").strip().lower()
            items = item_manager.search_item(search_term)
            if items:
                table = Table(title="Hasil Pencarian Barang")
                table.add_column("Nama Barang", style="cyan", justify="center")
                table.add_column("Kategori", style="magenta")
                table.add_column("Stok", style="green", justify="right")

                for item_name, item in items.items():
                    table.add_row(item_name, item['category'], str(item['stock']))

                console.print(table)
            else:
                console.print("[bold red]❌ Barang tidak ditemukan.[/bold red]")
            input("Tekan Enter untuk lanjut...")

        elif choice == '6':
            while True:  
                console.print("[bold cyan]Menu Sorting Barang[/bold cyan]")
                console.print("""
        [bold green]1.[/bold green] Sort berdasarkan Nama (A-Z)
        [bold green]2.[/bold green] Sort berdasarkan Harga (Termurah)
        [bold green]3.[/bold green] Sort berdasarkan Stok (Terkecil)
        [bold green]4.[/bold green] Kembali ke Menu Utama
        """)
                
                sort_choice = Prompt.ask("Pilih opsi untuk sorting", choices=["1", "2", "3", "4"], default="1")
                
                if sort_choice == '4':
                    break  
                
                sorted_items = None
                sort_title = ""
                
                if sort_choice == '1':
                    sorted_items = item_manager.get_sorted_items(by="name")
                    sort_title = "Barang Diurutkan berdasarkan Nama (A-Z)"
                elif sort_choice == '2':
                    sorted_items = item_manager.get_sorted_items(by="price")
                    sort_title = "Barang Diurutkan berdasarkan Harga (Termurah)"
                elif sort_choice == '3':
                    sorted_items = item_manager.get_sorted_items(by="stock")
                    sort_title = "Barang Diurutkan berdasarkan Stok (Terkecil)"
                
                if sorted_items:
                    table = Table(title=sort_title)
                    table.add_column("Nama Barang", style="cyan", justify="center")
                    table.add_column("Kategori", style="magenta")
                    table.add_column("Stok", style="green", justify="right")
                    table.add_column("Harga", style="yellow", justify="right")
                    
                    for item_name, item in sorted_items:
                        table.add_row(
                            item_name, 
                            item["category"], 
                            str(item["stock"]),
                            f"Rp {item['price']:,}"
                        )
                    
                    console.print(table)
                else:
                    console.print("[bold red]❌ Tidak ada barang untuk diurutkan.[/bold red]")
                
                input("Tekan Enter untuk kembali ke menu sorting...")

        elif choice == '7':
            menu_kategori(item_manager)

        elif choice == '8':
            break

        else:
            print("❌ Pilihan tidak valid.")
            

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
            input("Tekan Enter untuk lanjut...")

        elif choice == '2':
            category_name = validate_input("Masukkan nama kategori baru: ")

            if category_name in item_manager.get_all_categories().values():
                console.print(f"[bold red]❌ Kategori '{category_name}' sudah ada.[/bold red]")
            else:
                item_manager.add_category(category_name)
                console.print(f"[bold green]✅ Kategori '{category_name}' berhasil ditambahkan.[/bold green]")

            input("Tekan Enter untuk lanjut...")

        elif choice == '3':
            categories = item_manager.get_all_categories()
            if not categories:
                console.print("[bold red]❌ Tidak ada kategori untuk diedit![/bold red]")
                input("Tekan Enter untuk kembali...")
                continue
                
            Util.printTable("daftar items", item_manager, "categories")

            category_id = validate_input("Masukkan ID kategori yang ingin diedit: ")
            
            if category_id not in categories:
                console.print("[bold red]❌ ID kategori tidak ditemukan![/bold red]")
                input("Tekan Enter untuk kembali...")
                continue
            
            category_name = validate_input("Masukkan nama kategori baru: ")
            
            if category_name in categories.values():
                console.print(f"[bold red]❌ Kategori '{category_name}' sudah ada.[/bold red]")
            else:
                item_manager.edit_category(category_id, category_name)
                console.print("[bold green]✅ Kategori berhasil diperbarui.[/bold green]")
            
            input("Tekan Enter untuk lanjut...")

        elif choice == '4':
            categories = item_manager.get_all_categories()
            if not categories:
                console.print("[bold red]❌ Tidak ada kategori untuk dihapus![/bold red]")
                input("Tekan Enter untuk kembali...")
                continue
                
            Util.printTable("daftar items", item_manager, "categories")

            category_id = validate_input("Masukkan ID kategori yang ingin dihapus: ")
            
            if category_id not in categories:
                console.print("[bold red]❌ ID kategori tidak ditemukan![/bold red]")
            else:
                while True:
                    confirm = input(f"Apakah Anda yakin ingin menghapus kategori '{categories[category_id]}'? (y/n): ").strip().lower()
                    if confirm in ['y', 'n']:
                        break
                    console.print("[bold red]❌ Input harus 'y' atau 'n'![/bold red]")
                
                if confirm == 'y':
                    item_manager.delete_category(category_id)
                    console.print("[bold green]✅ Kategori berhasil dihapus.[/bold green]")
                else:
                    console.print("[yellow]⚠️ Penghapusan dibatalkan.[/yellow]")
            
            input("Tekan Enter untuk lanjut...")
            
        elif choice == '5':
            break

        else:
            console.print("[bold red]❌ Pilihan tidak valid.[/bold red]")

        
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
            employees = listDataUser.getDataByRole("employee")
            if not employees:
                console.print("[bold red]❌ Tidak ada karyawan untuk diedit![/bold red]")
                input("Tekan Enter untuk kembali...")
                continue
                
            Util.printTable("daftar karyawan", listDataUser, "employee")

            tempUsername = validate_input("Masukkan username yang ingin diedit: ")
            user = listDataUser.findUser(tempUsername)

            if user and user.role == "employee":
                console.print("[yellow]⚠️ Kosongkan input jika tidak ingin mengubah field tersebut.[/yellow]")

                fields = {
                    "username": f"Username baru [{user.username}]",
                    "nama": f"Nama baru [{user.name}]",
                    "email": f"Email baru [{user.email}]",
                    "password": f"Password baru [{user.password}]"
                }

                Util.editAllData(tempUsername, listDataUser, fields)
                console.print("[green]✅ Data karyawan berhasil diperbarui.[/green]")
            else:
                console.print("[red]❌ Username tidak ditemukan atau bukan karyawan![/red]")

            input("Tekan Enter untuk lanjut...")

        elif choice == "2":
            employees = listDataUser.getDataByRole("employee")
            if not employees:
                console.print("[bold red]❌ Tidak ada karyawan untuk dihapus![/bold red]")
                input("Tekan Enter untuk kembali...")
                continue
                
            Util.printTable("daftar karyawan", listDataUser, "employee")
            
            tempUsername = validate_input("Masukkan username yang ingin dihapus: ")
            user = listDataUser.findUser(tempUsername)
            
            if user and user.role == "employee":
                while True:
                    confirm = input(f"Apakah Anda yakin ingin menghapus karyawan '{user.name}'? (y/n): ").strip().lower()
                    if confirm in ['y', 'n']:
                        break
                    console.print("[bold red]❌ Input harus 'y' atau 'n'![/bold red]")
                
                if confirm == 'y':
                    listDataUser.deleteData(tempUsername)
                    console.print("[green]✅ Data karyawan berhasil dihapus.[/green]")
                else:
                    console.print("[yellow]⚠️ Penghapusan dibatalkan.[/yellow]")
            else:
                console.print("[red]❌ Username tidak ditemukan atau bukan karyawan![/red]")
            input("Tekan Enter untuk lanjut...")

        elif choice == "3":
            Util.printTable("daftar karyawan", listDataUser, "employee")
            input("Tekan Enter untuk lanjut...")

        elif choice == "4":
            break

        else:
            console.print("[red]❌ Pilihan tidak valid![/red]")
            input("Tekan Enter untuk lanjut...")

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
            suppliers = listDataUser.getDataByRole("supplier")
            if not suppliers:
                console.print("[bold red]❌ Tidak ada supplier untuk diedit![/bold red]")
                input("Tekan Enter untuk kembali...")
                continue
                
            Util.printTable("daftar supplier", listDataUser, "supplier")
            
            username = validate_input("Masukkan username supplier yang ingin diedit: ")
            supplier = listDataUser.findUser(username)
            
            if supplier and supplier.role == "supplier":
                console.print("[yellow]⚠️ Kosongkan input jika tidak ingin mengubah field tersebut.[/yellow]")

                fields = {
                    "username": f"Username baru [{supplier.username}]",
                    "nama": f"Nama baru [{supplier.name}]",
                    "email": f"Email baru [{supplier.email}]",
                    "password": f"Password baru [{supplier.password}]"
                }

                Util.editAllData(username, listDataUser, fields)
                console.print("[green]✅ Data supplier berhasil diperbarui.[/green]")
            else:
                console.print("[red]❌ Supplier tidak ditemukan![/red]")
            input("Tekan Enter untuk lanjut...")

        elif p == "2":
            suppliers = listDataUser.getDataByRole("supplier")
            if not suppliers:
                console.print("[bold red]❌ Tidak ada supplier untuk dihapus![/bold red]")
                input("Tekan Enter untuk kembali...")
                continue
                
            Util.printTable("daftar supplier", listDataUser, "supplier")
            
            username = validate_input("Masukkan username supplier yang akan dihapus: ")
            user = listDataUser.findUser(username)
            
            if user and user.role == "supplier":
                while True:
                    confirm = input(f"Apakah Anda yakin ingin menghapus supplier '{user.name}'? (y/n): ").strip().lower()
                    if confirm in ['y', 'n']:
                        break
                    console.print("[bold red]❌ Input harus 'y' atau 'n'![/bold red]")
                
                if confirm == 'y':
                    listDataUser.deleteData(username)
                    console.print("[green]✅ Supplier berhasil dihapus.[/green]")
                else:
                    console.print("[yellow]⚠️ Penghapusan dibatalkan.[/yellow]")
            else:
                console.print("[red]❌ Supplier tidak ditemukan![/red]")
            input("Tekan Enter untuk lanjut...")

        elif p == "3":
            Util.printTable("daftar supplier", listDataUser, "supplier")
            input("Tekan Enter untuk lanjut...")

        elif p == "4":
            suppliers = listDataUser.getDataByRole("supplier")
            if not suppliers:
                console.print("[bold red]❌ Tidak ada supplier tersedia![/bold red]")
                input("Tekan Enter untuk kembali...")
                continue
                
            Util.printTable("daftar supplier", listDataUser, "supplier")
            
            username = validate_input("Masukkan username supplier: ")
            user = listDataUser.findUser(username)
            
            if user and user.role == "supplier":
                console.print(f"[cyan]Username:[/cyan] {user.username}")
                console.print(f"[green]Nama:[/green] {user.name}")
                console.print(f"[blue]Email:[/blue] {user.email}")
                console.print(f"[magenta]Role:[/magenta] {user.role}")
            else:
                console.print("[red]❌ Supplier tidak ditemukan![/red]")
            input("Tekan Enter untuk lanjut...")

        elif p == "5":
            suppliers = listDataUser.getDataByRole("supplier")
            if not suppliers:
                console.print("[bold red]❌ Tidak ada supplier untuk disorting![/bold red]")
                input("Tekan Enter untuk kembali...")
                continue
                
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
            console.print("[red]❌ Pilihan tidak valid![/red]")
            input("Tekan Enter untuk lanjut...")
            
def menu_pembeli(listDataUser: UserManager):
    console = Console()
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]Menu Pembeli[/bold cyan]"))
        console.print("""
1. Edit Pembeli
2. Hapus Pembeli
3. Lihat Daftar Pembeli
4. Cari Data Pembeli
5. Sorting Data Pembeli
6. Kembali
""")
        p = Prompt.ask("[chartreuse1]Pilih menu: [/chartreuse1]")

        if p == "1":
            users = listDataUser.getDataByRole("user")
            if not users:
                console.print("[bold red]❌ Tidak ada peminjam untuk diedit![/bold red]")
                input("Tekan Enter untuk kembali...")
                continue
                
            Util.printTable("daftar peminjam", listDataUser, "user")
            
            username = validate_input("Masukkan username peminjam yang ingin diedit: ")
            peminjam = listDataUser.findUser(username)
            
            if peminjam and peminjam.role == "user":
                console.print("[yellow]⚠️ Kosongkan input jika tidak ingin mengubah nilai tersebut[/yellow]")
                fields = {
                    "username": f"Username baru [{peminjam.username}]",
                    "nama": f"Nama baru [{peminjam.name}]",
                    "email": f"Email baru [{peminjam.email}]",
                    "password": f"Password baru [{peminjam.password}]"
                }
                
                Util.editAllData(username, listDataUser, fields)
                console.print("[green]✅ Data peminjam berhasil diubah[/green]")
            else:
                console.print("[red]❌ Pembeli tidak ditemukan![/red]")
            input("Tekan Enter untuk lanjut...")

        elif p == "2":
            users = listDataUser.getDataByRole("user")
            if not users:
                console.print("[bold red]❌ Tidak ada peminjam untuk dihapus![/bold red]")
                input("Tekan Enter untuk kembali...")
                continue
                
            Util.printTable("daftar peminjam", listDataUser, "user")
            
            username = validate_input("Masukkan username peminjam yang akan dihapus: ")
            user = listDataUser.findUser(username)
            
            if user and user.role == "user":
                while True:
                    confirm = input(f"Apakah Anda yakin ingin menghapus peminjam '{user.name}'? (y/n): ").strip().lower()
                    if confirm in ['y', 'n']:
                        break
                    console.print("[bold red]❌ Input harus 'y' atau 'n'![/bold red]")
                
                if confirm == 'y':
                    listDataUser.deleteData(username)
                    console.print("[green]✅ Pembeli berhasil dihapus.[/green]")
                else:
                    console.print("[yellow]⚠️ Penghapusan dibatalkan.[/yellow]")
            else:
                console.print("[red]❌ Pembeli tidak ditemukan![/red]")
            input("Tekan Enter untuk lanjut...")

        elif p == "3":
            Util.printTable("daftar peminjam", listDataUser, "user")
            input("Tekan Enter untuk lanjut...")

        elif p == "4":
            users = listDataUser.getDataByRole("user")
            if not users:
                console.print("[bold red]❌ Tidak ada peminjam tersedia![/bold red]")
                input("Tekan Enter untuk kembali...")
                continue
                
            Util.printTable("daftar peminjam", listDataUser, "user")
            
            username = validate_input("Masukkan username peminjam: ")
            user = listDataUser.findUser(username)
            
            if user and user.role == "user":
                console.print(f"[cyan]Username:[/cyan] {user.username}")
                console.print(f"[green]Nama:[/green] {user.name}")
                console.print(f"[blue]Email:[/blue] {user.email}")
                console.print(f"[magenta]Role:[/magenta] {user.role}")
            else:
                console.print("[red]❌ Pembeli tidak ditemukan![/red]")
            input("Tekan Enter untuk lanjut...")

        elif p == "5":
            peminjam = listDataUser.getDataByRole("user")
            sorted_data = dict(sorted(peminjam.items()))
            table = Table(title="Pembeli Tersorting Berdasarkan Nama (A-Z)")
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
        else:
            console.print("[red]Pilihan tidak valid![/red]")
            input("Tekan Enter untuk lanjut...")


if __name__ == "__main__":
    userManager = UserManager("path/ke/file_user.json")
    itemManager = ItemsManager("path/ke/barang.json")
    main_menu(itemManager, userManager)
