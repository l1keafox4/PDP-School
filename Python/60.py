file = open('JOPA.txt', 'w')
file.write('JOPA, KOPA, GULP, LOX')

with open('JOPA.txt', 'r') as file:
    data = file.read()
    for lox in data:
        if lox == 'a' or lox == 'A':
            print('a', end=' ')
