from pwn import *
from Crypto.Util.number import *
import json
import codecs

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import math
import sympy

r = remote('socket.cryptohack.org', 13373)

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)
    
r.recvuntil("Intercepted from Alice: ")
res = json_recv()
p = int(res["p"], 16)
g = int(res["g"], 16)
A = int(res["A"], 16)
    
r.recvuntil("Intercepted from Bob: ")
res = json_recv()

r.recvuntil("Intercepted from Alice: ")
res = json_recv()
iv = res["iv"]
ciphertext = res["encrypted"]

#b'Intercepted from Alice: {"p": "0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff", "g": "0x02", "A": "0xf3e024f73ec8144f46ec7a2f4c699189857be26e8e1c1ad7e3ee6e5d14f4d2ba637479e9bd208571ccb8447d206e32a0893235975b121150fbc3eb429450f63e4145bd158e488701a1da2146b4052b4616407b262a3bacc15d8acaf2064b9a80c7b2c4c7e74fb5a3e5ca5a21074682031c9b0c92849bad3f3f009a5fffc9bfac66cad19ec04376fe2e3604ea0eb6e780764f0d3ac7b4127696dc772f88cd2f17523c4ed4aa11a62e8e6fd930304364458214209dcbd0c52b4982f91f18c749aa"}\n'
#b'Intercepted from Bob: {"B": "0x8d79b69390f639501d81bdce911ec9defb0e93d421c02958c8c8dd4e245e61ae861ef9d32aa85dfec628d4046c403199297d6e17f0c9555137b5e8555eb941e8dcfd2fe5e68eecffeb66c6b0de91eb8cf2fd0c0f3f47e0c89779276fa7138e138793020c6b8f834be20a16237900c108f23f872a5f693ca3f93c3fd5a853dfd69518eb4bab9ac2a004d3a11fb21307149e8f2e1d8e1d7c85d604aa0bee335eade60f191f74ee165cd4baa067b96385aa89cbc7722e7426522381fc94ebfa8ef0"}\n'
#b'Intercepted from Alice: {"iv": "ec44bd5b71b37e451dd8a07b5d327cd0", "encrypted": "a0b34652765f015862b130a9f57c1e7e7f11b9bab249bc98b3b30897ac5cf4d4"}\n'

r.recvuntil("send him some parameters: ")
json_send({
    "p": hex(p),
    "g": hex(A),
    "A": hex(1)
    })

r.recvuntil("Bob says to you: ")
res = json_recv()
shared_secret = int(res["B"], 16)

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