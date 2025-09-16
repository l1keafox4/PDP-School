# x = [2,3,4,5, "lox"]

# lox = iter(x)

# try:
#     print(next(lox))
#     print(next(lox))
#     print(next(lox))
#     print(next(lox))
#     print(next(lox))
#     print(next(lox))
# except StopIteration:
#     print("StopIteration qaytarildi")


# try:
#     for i in range(len(x)):
#         print(next(lox))
# except StopIteration:
#     print("StopIteration qaytarildi")


class Jopa:
    def __init__(self, limit=0):
        self.limit = limit
    def __iter__(self):
        self.n = 1
        return self
    def __next__(self):
        if self.n <= self.limit:
            kot_number= 2** self.n
            self.n += 1
            return kot_number
        else:
            raise StopIteration
        
numbers = Jopa(5)
iterator = iter(numbers)

print(next(iterator))
print(next(iterator))
print(next(iterator))
print(next(iterator))
print(next(iterator))