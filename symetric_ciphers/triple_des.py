import requests
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import long_to_bytes, bytes_to_long

def encrypt_flag(key):
    url = "http://aes.cryptohack.org/triple_des/encrypt_flag/"
    url += key.hex()
    url += "/"
    r = requests.get(url)
    js = r.json()
    return bytes.fromhex(js["ciphertext"])

def encrypt(key, plaintext):
    url = "http://aes.cryptohack.org/triple_des/encrypt/"
    url += key.hex()
    url += "/"
    url += plaintext.hex()
    url += "/"
    r = requests.get(url)
    js = r.json()
    return bytes.fromhex(js["ciphertext"])

def xor(a, b):
    return long_to_bytes(bytes_to_long(a) ^ bytes_to_long(b))

init_key = [b"\x00" * 8, b"\xff" * 8]

key = init_key[0] + init_key[1]

step1 = encrypt_flag(key)
step2 = encrypt(key, step1)

print(unpad(step2, 8))