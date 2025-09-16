class A:
    def __init__(self, name, cycle):
        self.name = name
        self.cycle = cycle

    def info(self):
        return self.name, self.cycle
    

class B(A):
    def __init__(self, name, cycle, color):
        super().__init__(name, cycle)
        self.color = color

    # def info(self):
    #     return f"{self.name}, {self.cycle}, {self.color}"

obj = B("krug","aylana","blaq")
print(obj.info())