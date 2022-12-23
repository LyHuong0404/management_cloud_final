class User:
    def __init__(self, name, password, admin):
        self.name = name
        self.password = password
       
        

    def toDBCollectionUser(self):
        return{
            'name': self.name,
            'password': self.password,      
        }