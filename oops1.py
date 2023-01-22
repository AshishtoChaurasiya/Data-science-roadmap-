class Person:
    def age(self, curre_year, year_of_birth):
        return curre_year - year_of_birth
    def email_id_input(self,email_id):
        print("take and mail id form a person and print it", email_id)
    def ask_name(self):
        name=input("tell me your name ")
        return name
    def ask_dob(self):
        dob = input("tell me your date of birth ")
        return dob
ashish=Person()
ashish.email_id_input('ashishgchaurasiya786@gmail.com')
print(ashish.ask_dob())