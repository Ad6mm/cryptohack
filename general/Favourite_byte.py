from binascii import unhexlify
from operator import xor

def xor(decoded, byte):
    result = b''
    for d in decoded:
        result += bytes([d ^ byte])
    try:
        return result.decode("utf-8")
    except:
        return "Incorrect data"
    

HIDDEN = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"

hidden_decoded = unhexlify(HIDDEN)

print("Decoded hidden: " + format(hidden_decoded))

for i in range(256):
    xor_result = xor(hidden_decoded, i)
    if 'crypto' in xor_result:
        print(xor_result)