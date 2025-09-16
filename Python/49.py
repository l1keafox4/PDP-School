class Person:
    def __init__(self, name, year, model):
        self.name = name
        self.year = year
        self.model = model
    @property
    def get_info(self):
        return self.name, self.year, self.model
        
    def change_info(self, year):
        new_year = int(input("New year:"))
        self.year = new_year

obj = Person(name='BMW', year=2011, model='i8')
print(*obj.get_info)
obj.change_info(obj.year)
print(*obj.get_info)