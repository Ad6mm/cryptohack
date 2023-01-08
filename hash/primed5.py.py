import json
from hashlib import md5
from Crypto.Util.number import *
from pwn import *
import math

m0 = bytes.fromhex("0e306561559aa787d00bc6f70bbdfe3404cf03659e704f8534c00ffb659c4c8740cc942feb2da115a3f4155cbb8607497386656d7d1f34a42059d78f5a8dd1ef")
m1 = bytes.fromhex("0e306561559aa787d00bc6f70bbdfe3404cf03659e744f8534c00ffb659c4c8740cc942feb2da115a3f415dcbb8607497386656d7d1f34a42059d78f5a8dd1ef")

assert md5(m0).hexdigest() == md5(m1).hexdigest()
counter = 0

while True:
 s = long_to_bytes(counter, 4)
 if isPrime(bytes_to_long(m0 + s)):
    break
 counter += 1
     
print("s: ", s)

p0 = m0 + s
p1 = m1 + s

assert md5(p0).hexdigest() == md5(p1).hexdigest()
assert isPrime(bytes_to_long(p0))
assert not isPrime(bytes_to_long(p1))

c = remote("socket.cryptohack.org", 13392)
c.recvline()

msg = {"option": "sign", "prime": str(bytes_to_long(p0))}

c.sendline(json.dumps(msg))
r = c.recvline()
sig = json.loads(r)["signature"]

a=1
while(a>bytes_to_long(p1) or math.gcd(a,bytes_to_long(p1)) < len("crypto{??????????????????}")):
 a=a+1
print("a",a)

msg = {
 "option": "check",
 "prime": str(bytes_to_long(p1)),
 "a": a,
 "signature": sig
}
c.sendline(json.dumps(msg))

flag = c.recvline()
print(flag)