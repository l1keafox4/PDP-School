class Student:
    def __init__(self, name , age , region):
        self.name = name
        self.age = age
        self.region = region
    
    def get_region(self):
        return self.region
    
    
    def get_all(self):
        return self.name , self.age , self.region
    
    
students = Student("Usmon", 10, "Tashkent")
print(students.get_region())
print(*students.get_all())