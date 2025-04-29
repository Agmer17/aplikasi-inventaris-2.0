# dashboard_admin.py
from rich.console import Console
from rich.panel import Panel

console = Console()

def main_menu():
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
            menu_barang()
        elif pilihan == "2":
            menu_kategori_barang()
        elif pilihan == "3":
            menu_karyawan()
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

def menu_barang():
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]Menu Barang[/bold cyan]"))
        console.print("""
1. Tambah Barang
2. Edit Barang
3. Hapus Barang
4. Lihat Daftar Barang
5. Cari
6. Sorting
7. Kelola Kategori Barang
8. Kembali
""")
        p = input("Pilih menu: ")
        if p == "7":
            menu_kategori_barang()
        elif p == "8":
            break


def menu_kategori_barang():
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]Menu Kategori Barang[/bold cyan]"))
        console.print("""
1. Lihat Daftar Kategori Barang
2. Tambah Kategori Barang
3. Edit Kategori Barang
4. Hapus Kategori Barang
5. Kembali
""")
        p = input("Pilih menu: ")
        if p == "5":
            break
        
def menu_karyawan():
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
        p = input("Pilih menu: ")
        if p == "7":
            break

def menu_supplier():
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
    console.clear()
    console.print(Panel.fit("[bold cyan]Registrasi Pengguna[/bold cyan]"))
    console.print("👉 Fungsi ini mengambil dari User.py di folder manager")
    input("Tekan Enter untuk kembali...")

def menu_laporan():
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
