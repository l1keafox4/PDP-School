# class Student:
#     def __init__(self, name, age, grade):
#         self.name = name
#         self.age = age
#         self.grade = grade

#     def student_info(self):
#         return f"Name: {self.name}, Age: {self.age}, Grade: {self.grade}"

class Students:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade

    def student_change(self, new_name, new_age, new_grade):
        self.name = new_name
        self.age = new_age
        self.grade = new_grade

    def student_info(self):
        return f"Name: {self.name}, Age: {self.age}, Grade: {self.grade}"
# name1 = input("Name: ")
# age1 = int(input("Age: "))
# grade1 = input("Grade: ")
# student1 = Student(name1, age1, grade1)
# info1 = student1.student_info()
# print(info1)

name2 = input("Name: ")
age2 = int(input("Age: "))
grade2 = input("Grade: ")
student2 = Students(name2, age2, grade2)

info1 = student2.student_info()
print(info1)

new_name2 = input("New name: ")
new_age2 = int(input("New age: "))
new_grade2 = input("New grade: ")
student2.student_change(new_name2, new_age2, new_grade2)

info2 = student2.student_info()
print(info2)