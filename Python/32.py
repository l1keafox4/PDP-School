# def kopa(a,b,c):
#     print(a*b*c)

# a = int(input(":"))
# b = int(input(":"))
# c = int(input(":"))

# kopa(a,b,c)

def sum(*args):
    my_sum = 1
    for i in args:
        my_sum*=i
    print(my_sum)
    return my_sum
a = int(input(":"))
b = int(input(":"))
c = int(input(":"))
sum(a,b,c)