import hashlib
from Crypto.Cipher import AES

def decrypt(ciphertext, password_hash):
    ciphertext = bytes.fromhex(ciphertext)
    key = password_hash

    cipher = AES.new(key, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        return {"error": str(e)}

    return decrypted

encrypted = "c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535ec0f4bbae66"

with open("symetric_ciphers/words.txt") as f:
    words = [w.strip() for w in f.readlines()]

for i in range(len(words)):
    KEY = hashlib.md5(words[i].encode()).digest()
    decrypted = decrypt(encrypted, KEY)
    try:
        decoded = decrypted.decode()
        if decoded[0] == 'c' and decoded[1] == 'r':
            print(decoded)
    except BaseException:
        continue