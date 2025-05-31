from module.User import Admin as AdminSchema
from module.User import Supplier as SupplierSchema
from module.User import Employee as EmployeeSchema
from module.User import User as UserSchema

import json

class UserManager:
    """
    Mengelola data pengguna dari file JSON.

    Fitur:
    - Tambah pengguna baru (register)
    - Hapus pengguna
    - Verifikasi login (username + password)
    - CRUD pengguna semua role! 
    - Load dan simpan data ke file JSON
    """
    
    @staticmethod
    def loadFile(path:str) -> dict[str:str] :
        '''static method buat load file dari path yang dikasih
        nanti path nya itu berupa absolute path biar gak error'''
        data = None
        try :
            with open(path, "r", encoding="utf-8") as files:
                data = json.load(files)
                return data
            
        except Exception as e:
            print("Error saat membaca file! harap perisa path nya! " + str(e))
            return {}
        
        
    @staticmethod
    def convertToClass(listData:dict[str:dict]) -> dict[str:object] :
        '''
        Static method buat convert data dari json yang berupa -> 
        
        value : {dict}
        
        jadi -> 
        
        value : Object
        
        ''' 
        data = {}
        
        for username, userData in listData.items() : 
            role = userData.get("role").lower()
            if role == "admin":
                data[username] = AdminSchema(username=username, **userData)
            if role == "employee":
                data[username] = EmployeeSchema(username=username, **userData)
            if role == "supplier":
                data[username] = SupplierSchema(username=username, **userData)
            if role == "user":
                data[username] = UserSchema(username=username, **userData)
            
        
        return data
    
    def __init__(self, path:str):
        '''
        pas class di inisiasi data dari json otomatis diubah jadi objek class
        '''
        self.path = path
        data = self.loadFile(self.path)
        self.items = self.convertToClass(data)
        
    
    def changeData(self) : 
        '''
        method buat overwrite file lama, bisa dipake buat 
        add data atau update data nanti
        '''
        listUserDummy = {}
        
        for data in self.items : 
            listUserDummy.update({data : self.findUser(data).getFullData()})
        
        try : 
            with open(self.path, mode="w") as files :
                json.dump(listUserDummy, files, indent=4)
        except Exception as e :
            print(e)
    
    def findUser(self, username: str) -> object:
        username_lower = username.lower()
        for key, user in self.items.items():
            if key.lower() == username_lower:
                return user  
        return None  

    
    def addData(self, dataUser:dict[str:str]) : 
        '''
        fungsi buat nambah data ke json. Format dict yang di parameter itu : 
        {
            name : nama,
            username : username,
            email : email,
            password : password,
            role : role
        }
        
        penentuan role bedasarkan key role dari parameter yg dikasih
        '''
        
        if self.findUser(dataUser.get("username")) == None :
            newUsers:object = None
            role:str = dataUser.get("role").lower()
            
            if role == "admin" :
                newUsers:AdminSchema = AdminSchema(**dataUser)
                
                self.items.update({dataUser.get("username") : newUsers})
            
            elif role == "employee" : 
                newUsers:EmployeeSchema = EmployeeSchema(**dataUser)
                
                self.items.update({dataUser.get("username") : newUsers})
                
            elif role == "supplier" : 
                newUsers:SupplierSchema = SupplierSchema(**dataUser)
                self.items.update({dataUser.get("username") : newUsers})
            
            elif role == "user" : 
                newUsers:UserSchema = UserSchema(**dataUser)
                self.items.update({dataUser.get("username") : newUsers})
            
            else : 
                print("role gak valid!")
                return False
            
            self.changeData()
            return True
        
        else : 
            print("username telah terdaftar, harap masukan username lain")
            return False
    
    def getDataByRole(self, paramUsername:str) -> dict[str: AdminSchema|EmployeeSchema|SupplierSchema| object] : 
        params = paramUsername.lower()
        temp = {}
        for key, value in self.items.items() : 
            if value.role == params :
                temp.update({value.username : value})
        return temp
    
    def deleteData(self, username:str) -> None:
        '''
        method buat menghapus data bedasarkan username.
        
        Args : 
            username(str) -> Username dari pengguna yang mau dihapus
        
        Execption : 
            jika pengguna gak ditemukan, exception akan menangkap error 
            berupa KeyError
        '''
        try:
            username_lower = username.lower()
            for key in list(self.items.keys()):
                if key.lower() == username_lower:
                    self.items.pop(key)
                    self.changeData()
                    print(f"Username '{key}' berhasil dihapus.")
                    return
            raise KeyError("Username tidak ditemukan")
        except Exception as e:
            print(f"Data username tidak ditemukan: {e}")
    
    def editUser(self, username: str, keyToChange: str, newValue: str):
        userToEdit = self.findUser(username)
        if userToEdit is None:
            print("username tidak ditemukan!")
            return

        keyToChange = keyToChange.lower()

        if not newValue:
            print("Tidak ada perubahan untuk field ini.")
            return

        key_in_items = None
        for key in self.items.keys():
            if key.lower() == username.lower():
                key_in_items = key
                break

        if key_in_items is None:
            print(f"Data username '{username}' sudah tidak ada.")
            return

        if keyToChange == "username":
            user_data = self.items.pop(key_in_items)
            user_data.changeUsername(newValue)
            self.items[newValue] = user_data
            print("Username berhasil diubah!")
        else:
            actions = {
                "nama": (userToEdit.changeName, "Nama berhasil diubah!"),
                "email": (userToEdit.changeEmail, "Email berhasil diubah!"),
                "password": (userToEdit.changePassword, "Password berhasil diubah!")
            }

            if keyToChange in actions:
                action_func, success_msg = actions[keyToChange]
                action_func(newValue)
                print(success_msg)
            else:
                print("Key nya tidak valid!")
                return

        self.changeData()


        
    def getAllData(self) -> dict[str:object] : 
        temp = {}
        
        for key, val in self.items.items() :
            temp.update({key : val.getFullData()})
        
        return temp


