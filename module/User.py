import time
class Person : 
    '''
    Class person tuh buat nampung data akun, soalnya dari 3 role 
    admin, karyawan dan suplier itu mereka punya kesamaan data dan method
    . Nanti pas di schema nya tinggal inherit aja ya, trs tambahin 
    method / data lain yg diperluin.
    
    nanti nyimpen data user di json nya pake nested dict => 
    {
        username : {
            nama : nama,
            email : Account.email,
            password : Account.password,
            role : Account.role
        },
    }
    
    cmn gua gatau ide bagus apa engga wkwkwk
    '''
    
    def __init__(self, name:str, username:str, email:str, password:str, role:str):
        self.id = f"USER-{int(time.time()*1000)}"
        self.name:str = name
        self.username:str = username
        self.email:str = email
        self.password:str = password
        self.role =role

    def _changeAtrribute(self, attributeName:str, newValue:str) -> bool :
        #isSameData tuh dia ngecek apakah value yg dimasukin sama
        #kayak data lama? kalo iya value nya gajadi diganti
        isNotSameData = (getattr(self, attributeName) != newValue)
        
        if isNotSameData: 
            setattr(self, attributeName, newValue)
            return True
        
        print(f"{attributeName} tidak boleh sama!")
        return False
    
    def changeName(self, newName:str) :
        return self._changeAtrribute("name", newName)
        
    def changeUsername(self, newUsername:str) :
        return self._changeAtrribute("username", newUsername)
        
    def changePassword(self, newPassword:str) :
        return self._changeAtrribute("password", newPassword)
        
    def changeEmail(self, newEmail:str) :
        return self._changeAtrribute("email", newEmail)
    
    def getData(self) -> dict[str:str] :
        '''
        method buat get data yang nantinya ditampilin
        '''
        return {"username" : self.username,
                "nama" : self.name,
                "email" : self.email,
                "role" : self.role
                }
    
    def getFullData(self) -> dict[str:str] :
        """
        method buat get full data dalam bentuk dict yang nanti bisa dipake buat nulis file ke json
        """
        return {
        "name": self.name,
        "email": self.email,
        "password": self.password,
        "role": self.role
    }
        


class Supplier(Person) : 
    
    def __init__(self, name, username, email, password, role):
        super().__init__(name, username, email, password, role)

class Admin(Person) :
    def __init__(self, name, username, email, password, role):
        super().__init__(name, username, email, password, role)

class Employee(Person) :
    def __init__(self, name, username, email, password, role):
        super().__init__(name, username, email, password, role)

class User(Person) :
    def __init__(self, name, username, email, password, role):
        super().__init__(name, username, email, password, role)



