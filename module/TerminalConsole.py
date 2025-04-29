"""
Console.py - Modul sederhana untuk menyediakan objek Console dari Rich

Modul ini menyediakan objek console Rich yang sudah dikonfigurasi dan
fungsi untuk membersihkan layar terminal.
"""

from rich.console import Console
import time
import os
import time

console = Console(highlight=False, record=True)

def reset_terminal_state():
    # Clear sistem operasi
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # ANSI escape sequence untuk reset
    print("\033[2J\033[H", end="", flush=True)
    
    # Clear Rich buffer
    if hasattr(console, '_buffer'):
        console._buffer.clear()
    
    # Clear Rich console dengan parameter tambahan
    console.clear()
    
    # Jeda kecil
    time.sleep(0.03)


