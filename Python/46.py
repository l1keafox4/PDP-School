class Car:
    def __init__(self, name, model, year):
        self.name = name
        self.model = model
        self.year = year

    @property
    def get_info(self):
        return self.name, self.model, self.year
    
my_car = Car("BMW", "i8", 2020)

class BMW(Car):
    def __init__(self, name, model, year, km, speed):
        super().__init__(name, model, year)
        self.km = km
        self.speed = speed

    @property
    def info(self):
        return self.name, self.model, self.km, self.year, self.speed

max_objects = BMW("BMW", "i8", 2020, 45000, 600)
print(*max_objects.info)