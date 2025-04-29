from module.dashboard import Autentikasi
from module.Manager.UserManager import UserManager

from module.dashboard.AdminDashboard import main_menu as admin_menu
from module.dashboard.EmployeeDashboard import employee_main_menu
from module.dashboard.SupplierDashboard import supplier_main_menu
from module.dashboard.UserDashboard import user_main_menu

data = UserManager("data/user.json")

currentUser = Autentikasi.login_screen(data)

if hasattr(currentUser, 'role'):
    role = currentUser.role.lower()
    if role == "admin":
        admin_menu()
    elif role == "employee":
        employee_main_menu()
    elif role == "supplier":
        supplier_main_menu()
    elif role == "user":
        user_main_menu()
    else:
        print(f"[ERROR] Role '{role}' tidak dikenali.")
else:
    print("[ERROR] Gagal membaca role dari user.")
