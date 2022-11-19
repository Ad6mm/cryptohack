from pwn import * # pip install pwntools
from Crypto.Util.number import *
import json
import codecs

ENCODINGS = [
    "base64",
    "hex",
    "rot13",
    "bigint",
    "utf-8",
]

r = remote('socket.cryptohack.org', 13377, level = 'debug')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)



for x in range(100):
    received = json_recv()
    print("Level: ")
    print(x+1) 

    print("Received type: ")
    type = received["type"]
    print(type)
    print("Received encoded value: ")
    value = received["encoded"]
    print(value)

    if type == "base64":
        decoded = base64.b64decode(value).decode('utf-8')
    elif type == "hex":
        decoded = bytes.fromhex(value).decode('utf-8')
    elif type == "rot13":
        decoded = codecs.decode(value, 'rot_13')
    elif type == "bigint":
        decoded = long_to_bytes(int(value, 16)).decode('utf-8')
    elif type == "utf-8":
        decoded = ''
        for b in value:
            decoded += chr(b)

    print("Decoded value: ")
    print(decoded)

    to_send = {"decoded": decoded}

    print("To send: ")
    print(to_send)

    json_send(to_send)

json_recv()