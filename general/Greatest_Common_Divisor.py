def gcd(a, b):
    rest = a % b
    while rest != 0:
        a = b
        b = rest
        rest = a % b
    return b

a = 66528
b = 52920
print(gcd(a, b))