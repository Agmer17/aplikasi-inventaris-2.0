from module.dashboard import Autentikasi
from module.Manager.UserManager import UserManager
from module.Manager.ItemsManager import ItemsManager

from module.dashboard.AdminDashboard import main_menu as admin_menu
from module.dashboard.EmployeeDashboard import menu_utama_employee
from module.dashboard.SupplierDashboard import supplier_main_menu
from module.dashboard.UserDashboard import user_main_menu

data = UserManager("data/user.json")
items = ItemsManager()
currentUser = Autentikasi.login_screen(data)

if hasattr(currentUser, 'role'):
    role = currentUser.role.lower()
    if role == "admin":
        admin_menu(item_manager=items, userManager=data)
    elif role == "employee":
        menu_utama_employee()
    elif role == "supplier":
        supplier_main_menu()
    elif role == "user":
        user_main_menu()
    else:
        print(f"[ERROR] Role '{role}' tidak dikenali.")
else:
    print("[ERROR] Gagal membaca role dari user.")
