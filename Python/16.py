# 1

# l = [1 , 2 , 3 , 4 , 5 , 6 , 7 , 8]

# a = sum(l) / len(l)
# print(a)

# 2

# ages = [5, 12, 17, 18, 24, 32, 19, 0, 21]
# ages1 = []

# for g in ages:
#     if g > 1:
#         oddiy_son = True
#         for i in range(2, int(g ** 0.5) + 1):
#             if g % i == 0:
#                 oddiy_son = False
#                 break
#         if oddiy_son:
#             ages1.append(g)
# print(*ages1)

# 3

# p = [2, 1, 3, 4, 5, 6, 2, 4, 3, 1, 5, 2, 4]


# o = {}
# for q in p:
#     if q in o:
#         o[q] += 1
#     else:
#         o[q] = 1

# print(o)

# 4

# son = input(": ").split()
# print("")
# son.sort()
# for num in son:
#     print(num, end=" ")

# 5

# proce = {
#     "ACME":45.23,
#     "AAPL":612.78,
#     "IBM":202.55,
#     "HPQ":37.20,
#     "FB":10.75
# }

# n = min(proce, key=proce.get)
# z = proce.values()
# print(n,':',min(z))
# print(*n)
# print(min(n))

# 6

# s = {"key":765,"num":200,"son":202,"num2":593}

# j = s.values()

# if 200 in j:
#     print('bor')
    
# else: 
#     print('yoq')

# 7
    
# localdict = {
#     "class": {
#         "student": {
#             "name": "Mike",
#             "marks": {
#                 "physics": 777,
#                 "location": 888
#             }
#         }
#     }
# }


# x = localdict["class"]["student"]["marks"]["physics"]

# print(x)

# 8

# portfolio = [
# {"name":"IBM","shares":100,"price":91.1},
# {"name":"AAPL","shares":50,"price":543.22},
# {"name":"FB","shares":200,"price":21.09},
# {"name":"HPQ","shares":35,"price":31.75},
# {"name":"YHOO","shares":45,"price":16.35},
# {"name":"ACME","shares":75,"price":115.34}
# ]

# for s in portfolio:
#     if s ['price'] < 40:
#         t = s.values()
#         print(*t)
        
# 9
    
# a = {10,40,59,78,88}  
# s = {45,59,88,70,32,10}

# f = a.intersection(s)
# print(f)

# 10

# d = {"yellow","red","black"}
# c = ["orange","blue","green"]
# kl = list(d)
# kl1 = kl + c
# print(kl1)
