import math

v = (4, 6, 2, 5)

size = 0
for i in range(len(v)):
    size += v[i]**2
    
print(math.sqrt(size))