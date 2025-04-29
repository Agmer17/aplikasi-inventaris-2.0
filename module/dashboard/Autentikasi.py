"""
Fungsi login_screen

Deskripsi:
    Fungsi ini menampilkan antarmuka login berbasis terminal dengan desain
    yang menarik secara visual. Fungsi akan menampilkan banner ASCII art,
    mengumpulkan kredensial pengguna, memvalidasi terhadap data pengguna
    yang tersimpan, dan memberikan umpan balik yang sesuai.

Parameter:
    listData (UserManager): Instansi dari kelas UserManager yang berisi data penggunna dan metode untuk verifikasi pengguna

Nilai Pengembalian:
    User | Admin | Employee | Supplier: Jika login berhasil, mengembalikan objek pengguna yang telah diautentikasi
    None: Jika login gagal (pengembalian implisit)

Alur Proses:
    1. Membersihkan layar konsol
    2. Menampilkan banner ASCII dan pesan selamat datang
    3. Meminta input username dan password dari pengguna
    4. Mencari pengguna dengan username yang dimasukkan
    5. Memverifikasi password
    6. Menampilkan hasil login (berhasil/gagal)
    7. Mengembalikan objek pengguna jika berhasil

Contoh Penggunaan:
    user_manager = UserManager()
    current_user = login_screen(user_manager)
    if current_user:
        # Lanjutkan ke menu utama
    else:
        # Tampilkpsi loginan o ulang
"""



from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.align import Align
import time
from module.TerminalConsole import console, reset_terminal_state
from module.Manager.UserManager import UserManager


def ascii_banner():
    banner = r"""
     _                      _             _     
(_)_ ____   _____ _ __ | |_ __ _ _ __(_)___ 
| | '_ \ \ / / _ \ '_ \| __/ _` | '__| / __|
| | | | \ V /  __/ | | | || (_| | |  | \__ \
|_|_| |_|\_/ \___|_| |_|\__\__,_|_|  |_|___/
    """
    return banner

def login_screen(listData: UserManager):
    console.clear()
    reset_terminal_state()

    # Tampilkan header dengan ASCII Art
    banner_panel = Panel.fit(ascii_banner(), style="bold #e5c07b", border_style="#e5c07b")
    console.print(Align.center(banner_panel))

    # Penjelasan di bawah logo
    subtitle = Text("Welcome to Terminal Login", style="bold white")
    console.print(Align.center(subtitle))

    console.print("\n")

    # Form input username dan password
    username = Prompt.ask("[bold green]> Enter your username")
    password = Prompt.ask("[bold green]> Enter your password", password=True)

    currentUser: object = listData.findUser(username)
    # Simulasi proses login
    console.print("\n[bold yellow]⏳ Logging in...[/bold yellow]")
    time.sleep(1)
    

    # Hasil login dummy
    if currentUser and password == currentUser.password:
        console.print(Panel.fit(f"✅ [bold green]Login successful, welcome [white]{username}[/white]![/bold green]", border_style="green"))
        return currentUser
        
    else:
        console.print(Panel.fit("❌ [bold red]Login failed! Invalid credentials.[/bold red]", border_style="red"))
        