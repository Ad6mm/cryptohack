import requests
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import long_to_bytes, bytes_to_long


def encrypt():
    url = "http://aes.cryptohack.org/bean_counter/encrypt/"
    r = requests.get(url)
    js = r.json()
    return bytes.fromhex(js["encrypted"])

def xor(a, b):
    xored = b""
    for i in range(len(a)):
        xored += (a[i] ^ b[i]).to_bytes(1, byteorder = "big")

    return xored

png_signature = "89504e470d0a1a0a0000000d49484452"
encrypted = encrypt()

key = xor(bytes.fromhex(png_signature), encrypted[:16])

f = open("symetric_ciphers/flag.png", 'wb')

for i in range(len(encrypted) // 16):
    f.write(xor(key, encrypted[i * 16: (i + 1) * 16]))

f.close()