from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import long_to_bytes, bytes_to_long
import requests

def response(byte_string):
	url = "http://aes.cryptohack.org/ecbcbcwtf/decrypt/"
	url += byte_string.hex()
	url += "/"
	r = requests.get(url)
	js = r.json()
	return bytes.fromhex(js["plaintext"])

def xor(a, b):
	return long_to_bytes(bytes_to_long(a) ^ bytes_to_long(b))

enc = bytes.fromhex("cc4623edd7cd957d26018b281f3a61cf892818a88601e0f687bc9fbcc197bcafeee8f10a147059853403c090e42efd08")

iv = enc[:16]
block1 = enc[16:32]
block2 = enc[32:]

decrypt_block1 = xor(response(block1), iv)
decrypt_block2 = xor(response(block2), block1)
print(decrypt_block1 + decrypt_block2)