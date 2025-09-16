# # my_tuple = 'Odil lox', 2020
# # my_tuple1 = 1,2,3,1,2
# # print(my_tuple)

# # hk = "Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"

# # print(hk[:3])
# # print(hk[0:1])
# # print(hk[2:3])
# # print(hk[4:5])
# # print(hk[6:7])
# # print("Пт" in hk)
# # print(len(hk))

# # print(my_tuple + my_tuple1)

# # print(my_tuple1.count(2))

# # print(hk.index("Вс"))

# # numbers = (3,3,5,1,2,4,7,6,3,8,9,10,11,5,3)

# # print(numbers.index(6))
# # print(numbers.count(3))


# # my_jopl = (1,2,4,5,3,6,7)
# # a, b, *c = my_jopl
# # print(a)
# # print(b)
# # print(c)

# other = (1,2,3,5, 'hillo')

# my_set1 = {1, 2, 3, "hello"}
# my_set1.add(4)
# print(my_set1)

# my_set2 = {"hello" "hello"}
# print(my_set2)

# my_set3 = {1, 2, 3, "hello"}
# rt = my_set3.clear()
# print(rt)

# my_set4 = {1, 2, 3, "hello"}
# tr =my_set4.copy()
# print(tr)

# my_set5 = {1, 2, 3, "hello"}
# gh = my_set5.difference()
# print(gh)

# my_set6 = {1, 2, 3, "hello"}
# lox = my_set6.difference_update()
# print(lox)

# my_set7 = {1, 2, 3, "hello"}
# xol = my_set7.discard(other)
# print(xol)

# my_set8 = {1, 2, 3, "hello"}
# jpol = my_set8.intersection()
# print(jpol)

# my_set9 = {1, 2, 3, "hello"}
# skim = my_set9.intersection_update()
# print(skim)


# my_set10 = {1, 2, 3, 'hello'}
# qut = my_set10.isdisjoint(other)
# print(qut)

# my_set11 = {1, 2, 3, "hello"}
# c = my_set11.issubset(other)
# print(c)


# my_set12 = {1, 2, 3, "hello"}
# r = my_set12.issuperset(other)
# print(r)

# my_set13 = {1, 2, 3, "hello"}
# j = my_set13.pop()
# print(j)

# my_set14 = {1, 2, 3, "hello"}
# m = my_set14.remove(1)
# print(m)

# my_set15 = {1, 2, 3, "hello"}
# y = my_set15.symmetric_difference(other)
# print(y)

# my_set16 = {1, 2, 3, "hello"}
# rat = my_set16.symmetric_difference_update(other)
# print(rat)

# my_set17 = {1, 2, 3, "hello"}
# popa = my_set17.union(other)
# print(popa)

# my_set18 = {1, 2, 3, "hello"}
# pipec = my_set18.update(other)
# print(pipec)

# tuple = (3, 4, 5, 6, 'hi', 'hello')
# print(tuple * 3)

# a = {"Assalomu alaykum ", 1, 2.5, }
# b = {"Valaykum alaykum ", 1, 2.5, }                #setni bi biriga qo`shish bunda bir xillarini chiqarmidi
# a.update(b)
# print(a)

# a = {"Assalomu alaykum ", 1, 2.5, }
# b = ["Valaykum alaykum ", 1, 2.5, ]                #setni bilan listni qo`shish`
# a.union(b)
# print(a)


# a = {"Assalomu alaykum ", 1, 2.5, }
# b = {"Valaykum alaykum ", 1, 2.5, }                #setni bir xil qatnashgan elementni olib tashlab chiqaradi
# a.symmetric_difference_update(b)
# print(a)


# a = {"Assalomu alaykum ", 1, 2.5, }
# b = {"Valaykum alaykum ", 1, 2.5, }                #bunda takrorni olib tashlab qolganini bitta qiladi
# c = b.symmetric_difference(a)
# print(c)


# a = {"Assalomu alaykum ", 1, 2.5, }
# b = {"Valaykum alaykum ", 1, 2.5, }                #o`chiradi
# a.remove(1)
# print(a)


# a = {"Assalomu alaykum ", 1, 2.5, }
# #b = {"Valaykum alaykum ", 1, 2.5, }                #bu funksiya o`zi xoxlaganini o`chiradi chunki set indexsiz
# a.pop()
# print(a)


# a = {"Assalomu alaykum ", 1, 2.5, }
# b = {"Valaykum alaykum ", 1, 2.5, }                #True False yani ikkalasi ham bir xil bo`lsa true 2xil bolsa false`
# c= a.issubset(b)
# print(c)


# a = {"Valaykum alaykum", 1, 2.5}
# b = {"Valaykum alaykum"}                #error
# c = a.isdisjoint(b)
# print(c)



# a = {"Assalomu alaykum ", 1, 2.5, }
# b = {"Valaykum alaykum ", 1, 2.5, }                #Ikkalasida ham bir xil borini chiqaradi
# a.intersection_update(b)
# print(a)




# a = {"Assalomu alaykum ", 1, 2.5, }
# #b = {"Valaykum alaykum ", 1, 2.5, }                #bu funksiya = remove
# a.discard(2.5)
# print(a)


# a = {"Assalomu alaykum ", 1, 2.5, }
# b = {"Valaykum alaykum ", 1, 2.5, }                #Ikkalasida ham yo`qini chiqaradi 
# a.difference_update(b)



# print(a)



# a = {"Assalomu alaykum ", 1, 2.5, }
# b = a.copy()                                                       #NUsxalaydi 

# print(a)



# a = {"Assalomu alaykum ", 1, 2.5, }
# a.add("Valaykum alaykum ")             #Qo`shish`

# print(a)