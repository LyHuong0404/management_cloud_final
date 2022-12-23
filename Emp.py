class Emp:
    def __init__(self, name, email, phone, address, total_projects, total_test_case, total_defects_found, total_defects_pending):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.total_projects = total_projects
        self.total_test_case = total_test_case
        self.total_defects_found = total_defects_found
        self.total_defects_pending = total_defects_pending
        

    def toDBCollectionEmp(self):
        return{
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'total_projects': self.total_projects,
            'total_test_case': self.total_test_case,
            'total_defects_found': self.total_defects_found,
            'total_defects_pending': self.total_defects_pending
        }