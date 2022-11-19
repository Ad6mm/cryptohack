v = [2, 6, 3]
w = [1, 0, 0]
u = [7, 7, 2] 

#2*v
result1 = []
for i in v:
    result1.append(2*i)

#2*v-w
result2 = []
for i in range(3):
    result2.append(result1[i]-w[i])

#3*(2*v-w)
result3 = []
for i in result2:
    result3.append(3*i)

#2*u
result4 = []
for i in u:
    result4.append(2*i)

result = 0
for i in range(3):
    result += result3[i]*result4[i]

print(result)