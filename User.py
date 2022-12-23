class User:
    def __init__(self, name, password, admin):
        self.name = name
        self.password = password
        self.admin = admin
       
        

    def toDBCollectionUser(self):
        return{
            'name': self.name,
            'password': self.password,      
        }