from pwn import *
from Crypto.Util.number import *
import json
import codecs

r = remote('socket.cryptohack.org', 13399)

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(msg):
    request = json.dumps(msg).encode()
    r.sendline(request)

r.recvline()

msg = {
    "option": "reset_password", 
    "token": "00" * 28
}

json_send(msg)
json_recv()

for i in range(256):
    password = ""
    if i > 0:
        password = 8 * chr(i)
    msg = {
        "option": "authenticate", 
        "password": password
    }
    json_send(msg)

    msg = json_recv()["msg"]

    print(i)
    print(msg)
    if msg != "Wrong password.":
        break