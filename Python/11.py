# n = [
#     13 , 53 ,52,
#     5, 19, 9, 3,
#     78, 94, 1, 12
# ]

# a,b,c,d,r,t,y,u,i,o,p = n 

# if p>a:
#     print(a)
    

# elif p>b:
#     print(b)
    
# elif p>c:
#     print(c)
    
# elif p>d:
#     print(d)
    
# elif p>r:
#     print(r)
    
# elif p>t:
#     print(t)
    
# elif p>y:
#     print(y)
    
# elif p>u:
#     print(u)
    
# elif p>i:
#     print(i)
    
# elif p>o:
#     print(o)

# else:
#     print(0)
    
# def yigindi(n, arr, k, l):
#     if k < 0 or l >= n or k > l:
#         return 0

#     total = 0
#     for i in range(k, l+1):
#         total += arr[i]

#     return total

# n = int(input("Massiv kiriting: "))
# arr = []

# for i in range(n):
#     element = int(input(f"{i+1}-elementni kiriting: "))
#     arr.append(element)

# k = int(input("K indeksini kiriting: "))
# l = int(input("L indeksini kiriting: "))

# result = yigindi(n, arr, k, l)
# print("Yig'indi:", result)

# n = 10
# arr = []
# for i in range(n):
#     element = int(input(f"Elementni kiriting: "))
#     arr.append(element)

# k = int(input("K indeksini kiriting: "))
# l = int(input("L indeksini kiriting: "))

# result = (n, arr, k, l)
# print("Orta arifmetik:", result)

n = [18 , 6 , 7 , 8 ,
     9 , 1 , 3 , 5 , 
     4 , 10 , 14]
n1 = []
n2 = []
for i in n:
    if i%2 == 0:
        n1.append(i)
        
    else:
        n2.append(i)
        
n2.reverse()
n2.sort()

n1.sort()
n1.reverse()

print(n1)
print(n2)