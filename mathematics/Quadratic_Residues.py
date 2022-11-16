p = 29
ints = [14, 6, 11]

for a in ints:
    for i in range(1, p):
        if (i**2)%p == a:
            print(i)