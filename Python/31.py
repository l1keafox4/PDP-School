def restoreString(s, indices):
    n = len(s)
    bol = [''] * n
    
    for i in range(n):
        bol[indices[i]] = s[i]

    return ''.join(bol)
s = "codeleet"
indices = [4, 5, 6, 7, 0, 2, 1, 3]
lol = restoreString(s, indices)
print(lol)