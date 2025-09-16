
# dic= {
#     "Name": "Jasur",
#     "Surname": "Zokirov",
#     "Age": "15 y.o.",
#     'Country': 'Uzbekistan'
# }
# print(dic.get('Name'))
# print(dic['Surname'])
# print(dic['Age'])
# print(dic.get('Country'))

# print(dic.keys())
# print(dic.values())
# print(dic.items())
# topurch = {
#     "1": 'Qurt' ,
#     "2": 'Non' ,
#     "3": 'Gosht' ,
#     "4": 'Bodring' ,
# }

# cost = {
#     'Qurt': 15000,
#     'Non': 12000,
#     'Gosht': 80000, 
#     'Bodring':20000     
#     # 'Pomidor': '18000 s`om '
# }
# print(*cost.values())

# print(topurch.get("1"))
# print(topurch.get("2"))
# print(topurch.get("3"))
# print(topurch.get("4"))

# print(cost.get("Qurt"))
# print(cost.get("Non"))
# print(cost.get("Gosht"))
# print(cost.get("Bodring"))

# for i in cost:
#     cost[i] += 4000
# print(*cost.values())

# print(*cost.keys())
# print(*cost.values())
# print(15000 + 12000 + 80000 + 20000, "so`m")
# topurch["4"]= 'Pomidor'

# print(topurch.get("1"))
# print(topurch.get("2"))
# print(topurch.get("3"))
# print(topurch.get("4"))

# print(cost.get("Qurt"))
# print(cost.get("Non"))
# print(cost.get("Gosht"))
# print(cost.get("Pomidor"))

# print("Qurt" in cost)
# print("Qurt" in topurch)


br = {
    'matematika': 5,
    'English': 5,
    'Python': 5
}

print(br)

for fan, baxo in br.items():
    print(fan, baxo)

br2 = {
    'Python': 5,
    'matematika': 5,
    'English': 5
}

# if br == br2:
#     print("Lug'atlar bir-biriga teng")
# else:
#     print("Lug'atlar bir-biriga teng emas")

# person = {'name': 'Phill', 'age': 22, 'salary': 3500.0}

# # ('salary', 3500.0) is inserted at the last, so it is removed.
# result = person.popitem()

# print('Return Value = ', result)
# print('person = ', person)

# marks = { 'Physics': 67, 'Chemistry': 72, 'Math': 89 }

# element = marks.pop('Chemistry')

# print('Popped Marks:', element)

# d = {1: "один", 2: "три"}
# d1 = {2: "два"}


# d.update(d1)

# print(d)

# d1 = {3: "три"}


# d.update(d1)

# print(d)