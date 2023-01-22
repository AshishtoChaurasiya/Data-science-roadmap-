from matplotlib.pyplot import cla


class Person():
    def __init__(self, name,surname,yob):
        self.name = name
        self.surname = surname
        self.yob = yob
ashish=Person("Ashish","Chaurasiya",1998)
print(ashish.name + ashish.surname)