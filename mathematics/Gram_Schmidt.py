def dot_product(a, b):
	result = 0
	for i in range(4):
		result += a[i] * b[i]
	return result

v = [0, 0, 0, 0]
v[0] = [4, 1, 3, -1]
v[1] = [2, 1, -3, 4]
v[2] = [1, 0, -2, 7]
v[3] = [6, 2, 9, -5]

for i in range(len(v)):
	for j in range(i):
		size = dot_product(v[j], v[j])
		inner = dot_product(v[i], v[j])

		for k in range(4):
			v[i][k] -= v[j][k] * inner / size

print(v[3][1])