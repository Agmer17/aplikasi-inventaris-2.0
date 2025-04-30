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
            print(data)
            listUserDummy.update({data : self.findUser(data).getFullData()})
            print(self.findUser(data))
            print("ini lagi iterasi")
        
        try : 
            with open(self.path, mode="w") as files :
                json.dump(listUserDummy, files, indent=4)
                print("operasi berhasil dilakukan")
        except Exception as e :
            print(e)
    
    def findUser(self, username:str) -> object : 
        
        # hati hati soalnya ini cuman pass refrensi memory, 
        # jadi kalo lu ngambil data dari sini trs lu rubah langsung, jadi ilang berubah juga
        
        return self.items.get(username)
    
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
        try :
            self.items.pop(username)
            self.changeData()
        except Exception as e:
            print(f"Data username tidak ditemukan : {e}")
    
    def editUser(self, username: str, keyToChange: str):
        userToEdit = self.findUser(username)

        if userToEdit is None:
            print("Username tidak ada!")
            print("Data tidak dirubah!")
            return

        keyToChange = keyToChange.lower()
        value = input(f"Masukan {keyToChange} yang baru: ")

        if keyToChange == "username":
            # Simpan referensi dulu
            user_data = self.items.pop(username)
            user_data.changeUsername(value)
            self.items[value] = user_data
            print("Username berhasil diubah!")

        elif keyToChange == "nama":
            userToEdit.changeName(value)
            print("Nama berhasil diubah!")

        elif keyToChange == "email":
            userToEdit.changeEmail(value)
            print("Email berhasil diubah!")

        elif keyToChange == "password":
            userToEdit.changePassword(value)
            print("Password berhasil diubah!")

        else:
            print("Key nya tidak valid!")
            return

        # Simpan perubahan ke file JSON
        self.changeData()
        
    def getAllData(self) -> dict[str:object] : 
        temp = {}
        
        for key, val in self.items.items() :
            temp.update({key : val.getFullData()})
        
        return temp



# from .Auth_schema import Person