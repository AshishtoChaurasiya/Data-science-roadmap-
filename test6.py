from matplotlib.pyplot import cla


class person:

    _name = "ashish" #protected
    __surname = "Chaurasiya" #private
    yob = 1998 #public

    def _age(self, current_year):
        return current_year - self.yob
    def __age1(self, current_year):
        return current_year - self.yob
obj = person()
print(obj._age(2022))
print(obj._person__age1(2022))
# inside the employ class
class employee(person):
    _name = "Ashish Chaurasiya"
    __surname = "Chaurasiya"
    yob = 1998

obj1 = employee()
print(obj1)
print(obj1.yob)
print(obj1._name)
print(obj1._employee__surname)