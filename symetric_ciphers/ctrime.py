import requests

def encrypt(plaintext):
    url = "http://aes.cryptohack.org/ctrime/encrypt/"
    url += plaintext.hex()
    url += "/"
    r = requests.get(url)
    js = r.json()
    return bytes.fromhex(js["ciphertext"])

flag = "crypto{"

while(1):
    base = len(encrypt((flag + chr(0)).encode()))
    for i in range(33, 127):
        if len(encrypt((flag + chr(i)).encode())) < base:
            flag += chr(i)
            break

    print(flag)
    if flag[-1] == "}":
        break