from pwn import *
from Crypto.Util.number import *
import json
import codecs

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import math
import sympy

r = remote('socket.cryptohack.org', 13380)

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

#b'Intercepted from Alice: {"p": "0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff", "g": "0x02", "A": "0x902ce484f83ef4dd13ec25f8421104f4f86fe47256d99cac4b00fe73542c7a63defb6891173134149dc2f5bdeac97ac0e7517b157741c1f14adee6261197ccf3755277c698ea0cb594c33ed67fbb6616a3cf6def5768f3c9d80c3304e5d0c51844558d84d691748d71e3407a7374cead01692035002648925b79092e4a35f7e68f109713dcc9225b9f46d0f77722a33867dc2852737c8d7d7572ec3b85cf2df50d7f6930fba041e593facc101f29c7b2a7ef017769efda5ef69e8832c8104dd2"}\n'
#b'Intercepted from Bob: {"B": "0x55a8fd13c676ca800a04f74b58b9c461caef1748ccaa35833fb3fa6ab7b90ef11c609d6d5f1069ff1157d7db6fe95c779b3720b5016013ad146885430d107982e2f0dd5aa4a500bfc597c5243e476b1572374961b6a8a1479f9cf2fd0443b7009a999cacd257d201226c79aae197fb52cc5a2c9c9b44d501347135365183157466fc521c243103355254384800fd3da99815d0a30559a6300db762482ca2880e31fb6388b9509ce114a078c209621121ac2df7559ca515a12c94311dd31624e4"}\n'
#b'Intercepted from Alice: {"iv": "372f03e370b127a47f320ce7238bc08f", "encrypted": "e6320f04ba723c70280d7e8df9f9a37ba4211ed0d6f290777992fa7baf76658d6a64995fbf6792cfea8f4bd1ab88fc4a"}\n'

r.recvuntil("Intercepted from Alice: ")
res = json_recv()
p = int(res["p"], 16)
g = int(res["g"], 16)
A = int(res["A"], 16)

r.recvuntil("Intercepted from Bob: ")
res = json_recv()
B = int(res["B"], 16)

r.recvuntil("Intercepted from Alice: ")
res = json_recv()
iv = res["iv"]
ciphertext = res["encrypted"]

a = A * pow(g, -1, p) % p

shared_secret = a * B % p

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

print(decrypt_flag(shared_secret, iv, ciphertext))