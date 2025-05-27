from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from module.Manager.ItemsManager import ItemsManager
from module.Manager.UserManager import UserManager
from module.Manager.TransactionManager import TransactionManager
from module.items import Item
from module.User import Supplier
import datetime

console = Console()

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
    
    def get_supplier_items(self):
        """
        Mendapatkan semua barang yang di-supply oleh supplier yang sedang login
        
        Returns:
            dict: Dictionary berisi barang-barang milik supplier
        """
        all_items = self.items_manager.get_all_items()
        supplier_items = {}
        
        for item_name, item_data in all_items.items():
            # Cek apakah supplier dari item ini sama dengan current supplier
            # Dalam JSON, supplier disimpan sebagai string nama supplier
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
        
        # Buat tabel untuk menampilkan barang
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
        """
        Menambahkan barang baru dengan supplier saat ini
        """
        console.print(Panel.fit("[bold green]Tambah Barang Baru[/bold green]"))
        
        try:
            # Input data barang
            name = Prompt.ask("Nama barang")
            
            # Cek apakah barang sudah ada
            if self.items_manager.get_item(name):
                console.print(f"[red]Barang '{name}' sudah ada dalam sistem![/red]")
                return
            
            # Tampilkan kategori yang tersedia
            categories = self.items_manager.get_all_categories()
            if categories:
                console.print("\n[cyan]Kategori yang tersedia:[/cyan]")
                for cat_id, cat_name in categories.items():
                    console.print(f"{cat_id}. {cat_name}")
                
                category_choice = Prompt.ask("Pilih ID kategori atau ketik kategori baru")
                category = categories.get(category_choice, category_choice)
            else:
                category = Prompt.ask("Kategori barang")
            
            stock = int(Prompt.ask("Jumlah stok", default="0"))
            price = float(Prompt.ask("Harga beli"))
            sell_price = float(Prompt.ask("Harga jual"))
            desc = Prompt.ask("Deskripsi barang", default="")
            status = Prompt.ask("Status barang", default="aktif", choices=["aktif", "non-aktif"])
            
            # Buat data item baru dengan format yang sesuai JSON
            item_data = {
                "name": name,
                "category": category,
                "stock": stock,
                "price": price,
                "sellPrice": sell_price,
                "desc": desc,
                "supplier": self.supplier_username,
                "status": status,
                "entrydate": datetime.datetime.now().isoformat()
            }
            
            # Simpan ke ItemsManager
            self.items_manager.add_item(name, item_data)
            console.print(f"[green]✅ Barang '{name}' berhasil ditambahkan![/green]")
            
        except ValueError as e:
            console.print(f"[red]❌ Input tidak valid: {e}[/red]")
        except Exception as e:
            console.print(f"[red]❌ Terjadi kesalahan: {e}[/red]")
    
    def edit_item(self):
        """
        Edit barang milik supplier
        """
        console.print(Panel.fit("[bold yellow]Edit Barang[/bold yellow]"))
        
        supplier_items = self.get_supplier_items()
        if not supplier_items:
            console.print("[yellow]Anda belum memiliki barang yang terdaftar.[/yellow]")
            return
        
        # Tampilkan daftar barang supplier
        console.print("\n[cyan]Barang Anda:[/cyan]")
        for i, item_name in enumerate(supplier_items.keys(), 1):
            console.print(f"{i}. {item_name}")
        
        try:
            choice = int(Prompt.ask("Pilih nomor barang yang akan diedit")) - 1
            item_names = list(supplier_items.keys())
            
            if 0 <= choice < len(item_names):
                selected_item_name = item_names[choice]
                item_data = supplier_items[selected_item_name]
                
                console.print(f"\n[cyan]Mengedit: {selected_item_name}[/cyan]")
                console.print("Tekan Enter untuk tidak mengubah nilai")
                
                # Edit fields
                new_name = Prompt.ask("Nama barang baru", default=selected_item_name)
                new_category = Prompt.ask("Kategori baru", default=item_data.get('category', ''))
                new_stock = Prompt.ask("Stok baru", default=str(item_data.get('stock', 0)))
                new_price = Prompt.ask("Harga beli baru", default=str(item_data.get('price', 0)))
                new_sell_price = Prompt.ask("Harga jual baru", default=str(item_data.get('sellPrice', 0)))
                new_desc = Prompt.ask("Deskripsi baru", default=item_data.get('desc', ''))
                new_status = Prompt.ask("Status baru", default=item_data.get('status', 'aktif'), 
                                      choices=["aktif", "non-aktif"])
                
                # Update data
                updated_data = item_data.copy()
                updated_data.update({
                    'name': new_name,
                    'category': new_category,
                    'stock': int(new_stock),
                    'price': float(new_price),
                    'sellPrice': float(new_sell_price),
                    'desc': new_desc,
                    'status': new_status
                })
                
                # Simpan perubahan
                self.items_manager.update_item(selected_item_name, updated_data)
                console.print(f"[green]✅ Barang berhasil diupdate![/green]")
                
            else:
                console.print("[red]Pilihan tidak valid![/red]")
                
        except (ValueError, IndexError) as e:
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
        
        # Tampilkan daftar barang supplier
        console.print("\n[cyan]Barang Anda:[/cyan]")
        for i, item_name in enumerate(supplier_items.keys(), 1):
            console.print(f"{i}. {item_name}")
        
        try:
            choice = int(Prompt.ask("Pilih nomor barang yang akan dihapus")) - 1
            item_names = list(supplier_items.keys())
            
            if 0 <= choice < len(item_names):
                selected_item_name = item_names[choice]
                
                if Confirm.ask(f"Apakah Anda yakin ingin menghapus '{selected_item_name}'?"):
                    self.items_manager.delete_item(selected_item_name)
                    console.print(f"[green]✅ Barang '{selected_item_name}' berhasil dihapus![/green]")
                else:
                    console.print("[yellow]Penghapusan dibatalkan.[/yellow]")
                    
            else:
                console.print("[red]Pilihan tidak valid![/red]")
                
        except (ValueError, IndexError) as e:
            console.print(f"[red]❌ Input tidak valid: {e}[/red]")

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
        pilihan = input("Masukkan pilihan (1-2): ")

        if pilihan == "1":
            menu_barang_supplier(dashboard)
        elif pilihan == "2":
            console.print("[bold red]Keluar dari aplikasi...[/bold red]")
            break
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")
            input("Tekan Enter untuk melanjutkan...")

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
[bold green]5.[/bold green] Kembali                     
""")
        pilihan = input("Masukkan pilihan (1-5): ")
        
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
            break
        else:
            console.print("[bold red]Pilihan tidak valid![/bold red]")
            input("Tekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    supplier_main_menu()
