fk = list(range(1,25))

evnum= []
oddnum= []

for i in fk:
    if i in fk:
        if i % 2 == 0:
            evnum.append(i)
        else:
            oddnum.append(i)
            
print(oddnum)
print(evnum)