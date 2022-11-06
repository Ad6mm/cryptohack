from operator import mod

m = 17
a = 3 ** 17

a_mod = mod(a, m)

print(a_mod)

a = 5 ** 17

a_mod = mod(a, m)

print(a_mod)

a = 7 ** 16

a_mod = mod(a, m)

print(a_mod)