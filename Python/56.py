# N = int(input("N: "))

# for i in range(1, N+1):
#     for j in range(1, i+1):
#         print(j, end=" ")
#     print()

# a = int(input("a="))
# b = int(input("b="))
# c = int(input("c="))

# if (a > 0 and b > 0 and c <= 0) or (a > 0 and b <= 0 and c > 0) or (a <= 0 and b > 0 and c > 0):
#     result = a + b + c
# else:
#     result = a * b * c

# print(result)

def count_s(satr):
    count = 0
    for belgi in satr:
        if belgi == '*':
            count += 1
    return count

input_satr = input(": ")

natija = count_s(input_satr)

print(natija)
