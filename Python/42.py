class Car:
    def __init__(self, brand , year , price):
         self.brand = brand
         self.year = year
         self.price = price
             
    def get_brand(self):
        return self.brand
    
    
    def get_all(self):
        return self.brand , self.year , self.price
    

car = Car("BMW i8 Orange White Black", 2018 , "1 285 601 236 so`m")

print(car.get_brand())
print(*car.get_all())