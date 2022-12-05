from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes, bytes_to_long
import requests

encryptedFlag = bytes.fromhex("c41e0126df29ef8ef79cfa90023e8d44c800d8bc91230e7833a20006f005fb2eedad6072f900a09099d6398564c38a06e9")

def encrypt(plaintext, iv):
    url = "http://aes.cryptohack.org/symmetry/encrypt/"
    url += plaintext.hex()
    url += "/"
    url += iv.hex()
    url += "/"
    r = requests.get(url)
    js = r.json()
    return bytes.fromhex(js["ciphertext"])

def xor(a, b):
    return long_to_bytes(bytes_to_long(a) ^ bytes_to_long(b))

iv = encryptedFlag[:16]
flag = encryptedFlag[16:]

plaintext = b'\x00' * len(flag)

print(xor(encrypt(plaintext, iv), flag))

AES.new()