class Student:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
    @staticmethod
    def to_title(name):
        return name.title()
    
object = Student("xasan","silla",15)

print(object.to_title("xasan"))