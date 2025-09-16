def zachem() -> None:
    yield 1**2
    yield 10**2
    yield 0**2
    yield 3**2
    yield 9**2


gen = zachem()
try:
    print(next(gen))
    print(next(gen))
    print(next(gen))
    print(next(gen))
    print(next(gen))

except StopIteration:
    print("StopIteration")

op = [5,9,2,4,7,9]

qloq = iter(op)

try:
    while True:
        print(next(qloq))
except StopIteration:
    print('StopIteration')

def xz():
    yield 1
    yield 2
    yield 3

lox = xz()

for l in lox:
    print(l)
