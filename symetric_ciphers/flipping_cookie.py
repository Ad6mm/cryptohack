import requests
from Crypto.Cipher import AES
import os
from Crypto.Util.number import long_to_bytes, bytes_to_long

def response(cookie, iv):
    url = "http://aes.cryptohack.org/flipping_cookie/check_admin/"
    url += cookie.hex()
    url += "/"
    url += iv.hex()
    url += "/"
    r = requests.get(url)
    js = r.json()
    print(js)

cookie = bytes.fromhex("27ed71cb3bab21058b230901ca4cf40f4879fc6474bbd83b4a71e7e9980021be3962204cd4d0bb83e835b409402b5e48")

def xor(a, b):
    return long_to_bytes(bytes_to_long(a) ^ bytes_to_long(b))

origin = b'admin=False;expi'
target = b'admin=True;\x05\x05\x05\x05\x05'

iv = cookie[:16]
block1 = cookie[16:32]
block2 = cookie[32:]

new_iv = xor(xor(origin, target), iv)

response(block1, new_iv)