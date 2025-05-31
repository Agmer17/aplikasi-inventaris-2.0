from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from module.Manager.ItemsManager import ItemsManager
from module.Manager.UserManager import UserManager
from module.Manager.TransactionManager import TransactionManager
from module.items import Item
from module.User import Supplier
from datetime import datetime
from module.transaction import Transaction

console = Console()
transaction = TransactionManager();

def validate_input(prompt_text, allow_empty=False, input_type="string", choices=None):
    """
    Fungsi untuk memvalidasi input dari pengguna
    
    Args:
        prompt_text: Teks prompt untuk user
        allow_empty: Apakah input boleh kosong
        input_type: Tipe input ("string", "int", "float")
        choices: List pilihan valid (untuk validasi pilihan)
    """
    while True:
        user_input = input(prompt_text).strip()
        
        if not allow_empty and not user_input:
            console.print("[bold red]❌ Input tidak boleh kosong![/bold red]")
            continue
        
        if allow_empty and not user_input:
            return user_input
            
        if choices and user_input not in choices:
            console.print(f"[bold red]❌ Pilihan harus salah satu dari: {', '.join(choices)}[/bold red]")
            continue
            
        if input_type == "int":
            try:
                value = int(user_input)
                if value < 0:
                    console.print("[bold red]❌ Angka tidak boleh negatif![/bold red]")
                    continue
                return value
            except ValueError:
                console.print("[bold red]❌ Input harus berupa angka bulat![/bold red]")
                continue
        
        elif input_type == "float":
            try:
                value = float(user_input)
                if value < 0:
                    console.print("[bold red]❌ Angka tidak boleh negatif![/bold red]")
                    continue
                return value
            except ValueError:
                console.print("[bold red]❌ Input harus berupa angka![/bold red]")
                continue
        
        return user_input

class SupplierDashboard:
    def __init__(self, supplier_username: str, supplier_name: str):
        """
        Initialize dashboard dengan supplier yang sedang login
        
        Args:
            supplier_username: Username supplier yang sedang login (key dari user.json)
            supplier_name: Nama supplier yang sedang login
        """
        self.supplier_username = supplier_username
        self.supplier_name = supplier_name
        self.items_manager = ItemsManager()
        self.transaction_manager = TransactionManager()  # Inisialisasi di sini
    
    def get_supplier_items(self):
        """
        Mendapatkan semua barang yang di-supply oleh supplier yang sedang login
        
        Returns:
            dict: Dictionary berisi barang-barang milik supplier
        """
        all_items = self.items_manager.get_all_items()
        supplier_items = {}
        
        for item_name, item_data in all_items.items():
            item_supplier = item_data.get('supplier', '')
            if item_supplier == self.supplier_username:
                supplier_items[item_name] = item_data
        
        return supplier_items
    
    def show_supplier_items(self):
        """
        Menampilkan daftar barang milik supplier dalam bentuk tabel
        """
        supplier_items = self.get_supplier_items()
        
        if not supplier_items:
            console.print("[yellow]Anda belum memiliki barang yang terdaftar dalam sistem.[/yellow]")
            return
        
        table = Table(title=f"Daftar Barang - {self.supplier_name}")
        table.add_column("Nama Barang", style="cyan")
        table.add_column("Kategori", style="magenta")
        table.add_column("Stok", style="green")
        table.add_column("Harga Beli", style="yellow")
        table.add_column("Harga Jual", style="red")
        table.add_column("Status", style="blue")
        table.add_column("Tanggal Entry", style="white")
        
        for item_name, item_data in supplier_items.items():
            table.add_row(
                item_name,
                item_data.get('category', 'N/A'),
                str(item_data.get('stock', 0)),
                f"Rp {item_data.get('price', 0):,.0f}",
                f"Rp {item_data.get('sellPrice', 0):,.0f}",
                item_data.get('status', 'N/A'),
                item_data.get('entrydate', 'N/A')[:10] if item_data.get('entrydate') else 'N/A'
            )
        
        console.print(table)
    
    def add_item(self):
        console.print(Panel.fit("[bold green]Tambah Barang Baru[/bold green]"))

        try:
            while True:
                name = validate_input("Masukkan nama barang: ", allow_empty=False)
                if self.items_manager.get_item(name):
                    console.print(f"[red]❌ Barang '{name}' sudah ada dalam sistem![/red]")
                    continue
                break

            categories = self.items_manager.get_all_categories()
            if not categories:
                console.print("[bold red]❌ Tidak ada kategori tersedia.[/bold red]")
                input("Tekan Enter untuk kembali...")
                return

            console.print("\n[cyan]Kategori yang tersedia:[/cyan]")
            for cat_id, cat_name in categories.items():
                console.print(f"{cat_id}. {cat_name}")

            category_id = validate_input("Masukkan ID kategori: ", allow_empty=False)
            category_name = categories.get(category_id)
            if not category_name:
                console.print("[bold red]❌ ID kategori tidak valid![/bold red]")
                input("Tekan Enter untuk kembali...")
                return

            stock = validate_input("Masukkan jumlah stok: ", input_type="int")
            price = validate_input("Masukkan harga beli: ", input_type="float")
            sell_price = validate_input("Masukkan harga jual: ", input_type="float")
            desc = validate_input("Masukkan deskripsi barang (opsional): ", allow_empty=True)
            status = validate_input("Masukkan status (aktif/non-aktif): ", allow_empty=False, choices=["aktif", "non-aktif"])

            item_data = {
                "name": name,
                "category": category_name,
                "stock": stock,
                "price": price,
                "sellPrice": sell_price,
                "entrydate": datetime.now().isoformat(),
                "desc": desc,
                "supplier": self.supplier_username,
                "status": status
            }

            self.items_manager.add_item(name, item_data)
            import uuid
            transaction_obj = Transaction(
                id=str(uuid.uuid4()),
                itemName=name,
                type="masuk",
                quantity=stock,
                pricePerItem=price,
                supplier=self.supplier_username,
                customer=None,
                notes="Penambahan barang baru",
                date=datetime.now().isoformat()
            )

            self.transaction_manager.add_transaction(transaction_obj)

            console.print(f"[green]✅ Barang '{name}' berhasil ditambahkan![/green]")
            console.print(f"[cyan]Stok: {stock} unit[/cyan]")
            console.print(f"[yellow]Harga beli: Rp {price:,.0f}[/yellow]")
            console.print(f"[red]Harga jual: Rp {sell_price:,.0f}[/red]")

        except Exception as e:
            console.print(f"[red]❌ Terjadi kesalahan: {e}[/red]")

        input("Tekan Enter untuk melanjutkan...")

    def edit_item(self):
        """
        Edit barang milik supplier
        """
        console.print(Panel.fit("[bold yellow]Edit Barang[/bold yellow]"))
        
        supplier_items = self.get_supplier_items()
        if not supplier_items:
            console.print("[yellow]Anda belum memiliki barang yang terdaftar.[/yellow]")
            return
        
        console.print("\n[cyan]Barang Anda:[/cyan]")
        item_names = list(supplier_items.keys())
        for i, item_name in enumerate(item_names, 1):
            console.print(f"{i}. {item_name}")
        
        try:
            choice = validate_input("Pilih nomor barang yang akan diedit: ", allow_empty=False, input_type="int") - 1
            
            if 0 <= choice < len(item_names):
                selected_item_name = item_names[choice]
                item_data = supplier_items[selected_item_name]
                
                console.print(f"\n[cyan]Mengedit: {selected_item_name}[/cyan]")
                console.print("Kosongkan untuk menggunakan nilai default")
                
                new_name = validate_input(f"Nama barang baru (default: {selected_item_name}): ", allow_empty=True)
                if not new_name:
                    new_name = selected_item_name
                
                current_category = item_data.get('category', '')
                new_category = validate_input(f"Kategori baru (default: {current_category}): ", allow_empty=True)
                if not new_category:
                    new_category = current_category
                
                current_stock = str(item_data.get('stock', 0))
                stock_input = validate_input(f"Stok baru (default: {current_stock}): ", allow_empty=True)
                if stock_input:
                    new_stock = validate_input("", allow_empty=False, input_type="int") if stock_input else int(current_stock)
                else:
                    new_stock = int(current_stock)
                
                current_price = str(item_data.get('price', 0))
                price_input = validate_input(f"Harga beli baru (default: {current_price}): ", allow_empty=True)
                if price_input:
                    try:
                        new_price = float(price_input)
                        if new_price < 0:
                            console.print("[red]❌ Harga tidak boleh negatif![/red]")
                            return
                    except ValueError:
                        console.print("[red]❌ Harga harus berupa angka![/red]")
                        return
                else:
                    new_price = float(current_price)
                
                current_sell_price = str(item_data.get('sellPrice', 0))
                sell_price_input = validate_input(f"Harga jual baru (default: {current_sell_price}): ", allow_empty=True)
                if sell_price_input:
                    try:
                        new_sell_price = float(sell_price_input)
                        if new_sell_price < 0:
                            console.print("[red]❌ Harga tidak boleh negatif![/red]")
                            return
                    except ValueError:
                        console.print("[red]❌ Harga harus berupa angka![/red]")
                        return
                else:
                    new_sell_price = float(current_sell_price)
                
                current_desc = item_data.get('desc', '')
                new_desc = validate_input(f"Deskripsi baru (default: {current_desc}): ", allow_empty=True)
                if not new_desc:
                    new_desc = current_desc
                
                current_status = item_data.get('status', 'aktif')
                new_status = validate_input(f"Status baru (aktif/non-aktif, default: {current_status}): ", allow_empty=True, choices=["aktif", "non-aktif", ""])
                if not new_status:
                    new_status = current_status
                
                updated_data = item_data.copy()
                updated_data.update({
                    'name': new_name,
                    'category': new_category,
                    'stock': new_stock,
                    'price': new_price,
                    'sellPrice': new_sell_price,
                    'desc': new_desc,
                    'status': new_status
                })
                
                self.items_manager.update_item(selected_item_name, updated_data)
                console.print(f"[green]✅ Barang berhasil diupdate![/green]")
                
            else:
                console.print("[red]❌ Pilihan tidak valid![/red]")
                
        except Exception as e:
            console.print(f"[red]❌ Input tidak valid: {e}[/red]")
    
    def delete_item(self):
        """
        Hapus barang milik supplier
        """
        console.print(Panel.fit("[bold red]Hapus Barang[/bold red]"))
        
        supplier_items = self.get_supplier_items()
        if not supplier_items:
            console.print("[yellow]Anda belum memiliki barang yang terdaftar.[/yellow]")
            return
        
        console.print("\n[cyan]Barang Anda:[/cyan]")
        item_names = list(supplier_items.keys())
        for i, item_name in enumerate(item_names, 1):
            console.print(f"{i}. {item_name}")
        
        try:
            choice = validate_input("Pilih nomor barang yang akan dihapus: ", allow_empty=False, input_type="int") - 1
            
            if 0 <= choice < len(item_names):
                selected_item_name = item_names[choice]
                
                confirm = validate_input(f"Apakah Anda yakin ingin menghapus '{selected_item_name}'? (y/n): ", allow_empty=False, choices=["y", "n", "Y", "N"])
                
                if confirm.lower() == 'y':
                    self.items_manager.delete_item(selected_item_name)
                    console.print(f"[green]✅ Barang '{selected_item_name}' berhasil dihapus![/green]")
                else:
                    console.print("[yellow]Penghapusan dibatalkan.[/yellow]")
                    
            else:
                console.print("[red]❌ Pilihan tidak valid![/red]")
                
        except Exception as e:
            console.print(f"[red]❌ Input tidak valid: {e}[/red]")
            
        
    def menu_sorting_barang(self):
        """
        Menyortir barang milik supplier berdasarkan kriteria tertentu.
        """
        console.print("\n[bold green]-- Sorting Barang Anda --[/bold green]")
        console.print("""
    [bold green]1.[/bold green] Urutkan berdasarkan Nama (A-Z)
    [bold green]2.[/bold green] Urutkan berdasarkan Harga Jual Termurah
    [bold green]3.[/bold green] Urutkan berdasarkan Harga Jual Termahal
    [bold green]4.[/bold green] Kembali
    """)
        
        pilihan = validate_input("Pilih opsi (1-4): ", allow_empty=False, choices=["1", "2", "3", "4"])

        supplier_items = self.get_supplier_items()
        
        if not supplier_items:
            console.print("[yellow]Anda belum memiliki barang.[/yellow]")
            return

        if pilihan == "1":
            sorted_items = dict(sorted(supplier_items.items()))
        elif pilihan == "2":
            sorted_items = dict(sorted(supplier_items.items(), key=lambda x: x[1].get('sellPrice', 0)))
        elif pilihan == "3":
            sorted_items = dict(sorted(supplier_items.items(), key=lambda x: x[1].get('sellPrice', 0), reverse=True))
        elif pilihan == "4":
            return

        table = Table(title="Barang Anda - Hasil Sorting")
        table.add_column("Nama Barang", style="cyan")
        table.add_column("Kategori", style="magenta")
        table.add_column("Stok", style="green")
        table.add_column("Harga Jual", style="red")

        for item_name, item_data in sorted_items.items():
            table.add_row(
                item_name,
                item_data['category'],
                str(item_data['stock']),
                f"Rp {item_data['sellPrice']:,}"
            )

        console.print(table)
        input("Tekan Enter untuk kembali...")
    
    def menu_cari_barang(self):
        console.print("\n[bold green]-- Cari Barang Anda --[/bold green]")
        
        search_term = validate_input("Masukkan nama barang yang dicari: ", allow_empty=False)
        
        supplier_items = self.get_supplier_items()
        hasil = {name: data for name, data in supplier_items.items() if search_term.lower() in name.lower()}
        
        if not hasil:
            console.print(f"[yellow]Tidak ditemukan barang dengan kata kunci '{search_term}'.[/yellow]")
            input("Tekan Enter untuk kembali...")
            return
        
        table = Table(title=f"Hasil Pencarian Barang Anda: '{search_term}'")
        table.add_column("Nama Barang", style="cyan")
        table.add_column("Kategori", style="magenta")
        table.add_column("Stok", style="green")
        table.add_column("Harga Beli", style="yellow")
        table.add_column("Harga Jual", style="red")

        for item_name, item in hasil.items():
            table.add_row(
                item_name,
                item['category'],
                str(item['stock']),
                f"Rp {item['price']:,}",
                f"Rp {item['sellPrice']:,}"
            )
        
        console.print(table)
        input("Tekan Enter untuk kembali...")


def supplier_main_menu(supplier_username: str, supplier_name: str):
    """
    Menu utama untuk supplier dashboard
    
    Args:
        supplier_username: Username supplier yang sedang login
        supplier_name: Nama supplier yang sedang login
    """
    dashboard = SupplierDashboard(supplier_username, supplier_name)
    
    while True:
        console.clear()
        console.print(Panel.fit(f"👋 [bold cyan]Selamat datang, {supplier_name}![/bold cyan]\nGunakan dashboard ini untuk mengelola data barang Anda dengan mudah.\nPilih fitur yang ingin dijalankan:", title="Dashboard Supplier"))
        console.print("""
[bold green]1.[/bold green] Kelola Barang
[bold green]2.[/bold green] Keluar App
""")
        pilihan = validate_input("Masukkan pilihan (1-2): ", allow_empty=False, choices=["1", "2"])

        if pilihan == "1":
            menu_barang_supplier(dashboard)
        elif pilihan == "2":
            console.print("[bold red]Keluar dari aplikasi...[/bold red]")
            break

def menu_barang_supplier(dashboard: SupplierDashboard):
    """
    Menu untuk mengelola barang supplier
    """
    while True:
        console.clear()
        console.print(Panel.fit(f"[bold cyan]Kelola Barang - {dashboard.supplier_name}[/bold cyan]"))
        console.print("""
[bold green]1.[/bold green] Tambah Barang
[bold green]2.[/bold green] Edit Barang
[bold green]3.[/bold green] Hapus Barang
[bold green]4.[/bold green] Lihat Daftar Barang
[bold green]5.[/bold green] Sorting Daftar Barang
[bold green]6.[/bold green] Cari Daftar Barang
[bold green]7.[/bold green] Kembali                     
""")
        pilihan = validate_input("Masukkan pilihan (1-7): ", allow_empty=False, choices=["1", "2", "3", "4", "5", "6", "7"])
        
        if pilihan == "1":
            dashboard.add_item()
            input("Tekan Enter untuk melanjutkan...")
        elif pilihan == "2":
            dashboard.edit_item()
            input("Tekan Enter untuk melanjutkan...")
        elif pilihan == "3":
            dashboard.delete_item()
            input("Tekan Enter untuk melanjutkan...")
        elif pilihan == "4":
            dashboard.show_supplier_items()
            input("Tekan Enter untuk melanjutkan...")
        elif pilihan == "5":
            dashboard.menu_sorting_barang()
        elif pilihan == "6":
            dashboard.menu_cari_barang()
        elif pilihan == "7":
            break

if __name__ == "__main__":
    supplier_main_menu()