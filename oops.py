class Person:
    def __init__(self, name,surname,emailid,year_of_birth):
        self.name= name
        self.surname = surname
        self.emailid = emailid
        self.year_of_birth = year_of_birth
    def age(self,current_year):
        return current_year - self.year_of_birth
ashish_var = Person("Ashish","Chaurasiya","chaurasiya1ashish@gmail.com",1998)
print(ashish_var.age(2022))
