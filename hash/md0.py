from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json

def bxor(a, b):
 return bytes(x ^ y for x, y in zip(a, b))


starter = b"a" * 16
p = remote('socket.cryptohack.org',13388)
payload = {"option": "sign", "message": starter.hex()}
p.sendline(json.dumps(payload))

s = p.recvline()
print("Line: ", s)

response = json.loads(p.recvline())
print(response)

signature = bytes.fromhex(response['signature'])
wanted = pad(b"admin=True",16)
print("Wanted: ", wanted)

sig = bxor(AES.new(wanted,AES.MODE_ECB).encrypt(signature),signature)
print("Signature: ", sig)

newmessage = pad(starter,16) + b"admin=True"
print("New message: ", newmessage)

payload = {"option": "get_flag", "message": newmessage.hex(),
"signature": sig.hex()}

p.sendline(json.dumps(payload))

print(p.recvline())