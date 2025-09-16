def generator():
    yield 1
    yield 2
    yield 3
    yield 4


gen = generator()
try:
    print(next(gen))
    print(next(gen))
    print(next(gen))
    print(next(gen))
    print(next(gen))
except StopIteration:
    print("StopIteration")
