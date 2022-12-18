from pwn import *
from Crypto.Util.number import *
import json
import codecs

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import math
import sympy

r = remote('socket.cryptohack.org', 13371)

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)
    
def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')
    
r.recvuntil("Intercepted from Alice: ")
res = json_recv()

print(res)

r.recvuntil("Send to Bob: ")
json_send({
    "p": hex(1),
    "g": hex(1),
    "A": hex(1)
    })

r.recvuntil("Intercepted from Bob: ")
res = json_recv()

r.recvuntil("Send to Alice: ")
json_send({
    "B": hex(1)
    })

r.recvuntil("Intercepted from Alice: ")
res = json_recv()

iv = res["iv"]
ciphertext = res["encrypted_flag"]

shared_secret = 1

print(decrypt_flag(shared_secret, iv, ciphertext))

r.interactive()