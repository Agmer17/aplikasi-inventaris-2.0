from module.dashboard import Autentikasi
from module.Manager.UserManager import UserManager

data = UserManager("data/user.json")
currentUser = Autentikasi.login_screen(data)