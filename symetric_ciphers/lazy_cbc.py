import requests
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Cipher import AES

def get_flag(key):
    url = "http://aes.cryptohack.org/lazy_cbc/get_flag/"
    url += key.hex()
    url += "/"
    r = requests.get(url)
    js = r.json()
    return bytes.fromhex(js["plaintext"])

def response(ciphertext):
    url = "http://aes.cryptohack.org/lazy_cbc/receive/"
    url += ciphertext.hex()
    url += "/"
    r = requests.get(url)
    js = r.json()
    return bytes.fromhex(js["error"][len("Invalid plaintext: "):])

def xor(a, b):
    return long_to_bytes(bytes_to_long(a) ^ bytes_to_long(b))

ciphertext = b"\x00" * 32
resp = response(ciphertext)
iv = resp[:16]
block = resp[16:]
print(get_flag(xor(iv, block)))