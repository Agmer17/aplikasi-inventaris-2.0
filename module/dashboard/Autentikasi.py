from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.align import Align
from rich import box
import time
from module.TerminalConsole import console, reset_terminal_state


def ascii_banner():
    banner = r"""
     _                      _             _     
(_)_ ____   _____ _ __ | |_ __ _ _ __(_)___ 
| | '_ \ \ / / _ \ '_ \| __/ _` | '__| / __|
| | | | \ V /  __/ | | | || (_| | |  | \__ \
|_|_| |_|\_/ \___|_| |_|\__\__,_|_|  |_|___/
    """
    return banner

def login_screen():
    console.clear()

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

    # Simulasi proses login
    console.print("\n[bold yellow]⏳ Logging in...[/bold yellow]")
    time.sleep(1)

    # Hasil login dummy
    if username == "admin" and password == "admin123":
        console.print(Panel.fit(f"✅ [bold green]Login successful, welcome [white]{username}[/white]![/bold green]", border_style="green"))
    else:
        console.print(Panel.fit("❌ [bold red]Login failed! Invalid credentials.[/bold red]", border_style="red"))
    reset_terminal_state()