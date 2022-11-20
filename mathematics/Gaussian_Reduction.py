v = [846835985, 9834798552] 
u = [87502093, 123094980]

def dot_product(a, b):
    result = 0
    for i in range(len(a)):
        result += a[i] * b[i]
    return result

def glr(a, b):
    if dot_product(b, b) < dot_product(a, a):
        glr(b, a)
        
    m = dot_product(a, b) // dot_product(a, a)
    
    if m == 0:
        return a, b
    
    tmp = []
    for i in a:
        tmp.append(m*i)
        
    for i in range(len(a)):
        b[i] = b[i] - tmp[i]
        
    return glr(a, b)


(a, b) = glr(v, u)
print(dot_product(a, b))