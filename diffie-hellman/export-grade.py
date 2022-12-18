from pwn import *
from Crypto.Util.number import *
import json
import codecs

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import math
import sympy

r = remote('socket.cryptohack.org', 13379)

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    #print(request)
    r.sendline(request)

r.recvuntil("Send to Bob: ")
json_send({"supported": ["DH64"]})

r.recvuntil("Send to Alice: ")
json_send({"chosen": "DH64"})

r.recvuntil("Intercepted from Alice: ")
res = json_recv()
print(res)

p = int(res["p"], 16)
g = int(res["g"], 16)
A = int(res["A"], 16)

a = sympy.ntheory.residue_ntheory.discrete_log(p, A, g)

r.recvuntil("Intercepted from Bob: ")
res = json_recv()
print(res)

B = int(res["B"], 16)

r.recvuntil("Intercepted from Alice: ")
res = json_recv()
print(res)

iv = res["iv"]
ciphertext = res["encrypted_flag"]

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


shared_secret = pow(B, a, p)

print(decrypt_flag(shared_secret, iv, ciphertext))

r.interactive()