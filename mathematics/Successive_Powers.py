from sympy.ntheory import factorint

results = [588, 665, 216, 113, 642, 4, 836, 114, 851, 492, 819, 237]
# p must be greater than 851 - max(results)

possible_p = [853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

# x = 209 - pen and sheet

m = 216 * 209 - 113

m_factored = factorint(m)

print(m_factored)

