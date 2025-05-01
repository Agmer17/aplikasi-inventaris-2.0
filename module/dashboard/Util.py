from module.Manager.ItemsManager import ItemsManager
from module.Manager.UserManager import UserManager
from rich.table import Table
from rich.console import Console

def userTable(title: str, data: UserManager, role: str) -> Table:
    temp: dict = data.getDataByRole(role)
    table = Table(title=title)
    table.add_column("Username", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Email", style="blue")
    table.add_column("Role", style="magenta")
    
    # Loop untuk menambahkan baris ke tabel
    for username, user in temp.items():
        table.add_row(username, user.name, user.email, user.role)
    
    return table


def itemTable(title:str, itemData:ItemsManager, type:str)  -> Table :
    
    if type == "items" : 
        items = itemData.get_all_items()
        table = Table(title=title)
        table.add_column("Nama Barang", style="cyan", justify="center")
        table.add_column("Kategori", style="magenta")
        table.add_column("Stok", style="green")

        for item_name, item in items.items():
            table.add_row(item_name, item['category'], str(item['stock']))
        return table

    elif type == "categories" : 
        # catgory table
        categoryTable = Table(title="Daftar Kategori")
        categoryTable.add_column("ID", style="cyan", justify="center")
        categoryTable.add_column("Nama Kategori", style="green")
        for category_id, category_name in itemData.get_all_categories().items():
            categoryTable.add_row(str(category_id), category_name)
            # -----------------------
        return categoryTable

def printTable(title: str, data: ItemsManager | UserManager, role: str | None) -> None:
    console = Console()
    
    # Validasi input tipe data
    if not (isinstance(data, ItemsManager) or isinstance(data, UserManager)):
        raise ValueError("Input gak valid! tolong masukan tipe data item atau user!")
    
    # Cek tipe data dan panggil fungsi yang sesuai
    if isinstance(data, UserManager):
        table = userTable(title, data, role)
        console.print(table)  # Cetak tabel
    else:
        
        if role not in ["categories", "items"] :
            raise ValueError("Input role gak valid! harap masukan items/category")
        items = itemTable(title, data, role)
        console.print(items)
        pass

# peminjam = listDataUser.getDataByRole("pembeli")
#             table = Table(title="Daftar Peminjam")
#             table.add_column("Username", style="cyan")
#             table.add_column("Name", style="green")
#             table.add_column("Email", style="blue")
#             table.add_column("Role", style="magenta")
#             for username, user in peminjam.items():
#                 table.add_row(username, user.name, user.email, user.role)
#             console.print(table)

# suppliers = listDataUser.getDataByRole("supplier")
#             table = Table(title="Daftar Supplier")
#             table.add_column("Username", style="cyan")
#             table.add_column("Name", style="green")
#             table.add_column("Email", style="blue")
#             table.add_column("Role", style="magenta")
#             for username, user in suppliers.items():
#                 table.add_row(username, user.name, user.email, user.role)
#             console.print(table)

# employees = listDataUser.getDataByRole("employee")
#             table = Table(title="Daftar Karyawan (Role: employee)")
#             table.add_column("Username", style="cyan")
#             table.add_column("Name", style="green")
#             table.add_column("Email", style="blue")
#             table.add_column("Password", style="red")
#             table.add_column("Role", style="magenta")

#             for username, user in employees.items():
#                 table.add_row(
#                     username,
#                     user.name,
#                     user.email,
#                     user.password,
#                     user.role
#                 )

# employees = listDataUser.getDataByRole("employee")
#             table = Table(title="Daftar Karyawan (Role: employee)")
#             table.add_column("Username", style="cyan")
#             table.add_column("Name", style="green")
#             table.add_column("Email", style="blue")
#             table.add_column("Password", style="red")
#             table.add_column("Role", style="magenta")

#             for username, user in employees.items():
#                 table.add_row(
#                     username,
#                     user.name,
#                     user.email,
#                     user.password,
#                     user.role
#                 )

# if __name__ == "__main__":
#     userManager = UserManager("path/ke/file_user.json")
#     itemManager = ItemsManager("path/ke/barang.json")
#     Console.print(printTable("data testing", userManager, "employee"))