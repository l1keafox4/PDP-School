def dec(func):
    def inner():
        print("Dec Ishladi") # noqa
        func()
        print("Dec toxtadi") # noqa
    return inner

# def funct():
#     print("Hello world!") # noqa


# deco = dec(funct)
# deco()

       

a = int(input("son: ")) # noqa
@dec
def decor():
    if a%2 == 0:
            print("juft") # jopa
    else:
            print("juftmas")

decor()