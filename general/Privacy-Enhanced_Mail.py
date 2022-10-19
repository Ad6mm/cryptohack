from base64 import b64decode
from Crypto.PublicKey import RSA

fileName = 'privacy_enhanced_mail_1f696c053d76a78c2c531bb013a92d4a.pem'

begin = '-----BEGIN RSA PRIVATE KEY-----'
end = '-----END RSA PRIVATE KEY-----'

f = open(fileName, "r")
fileContent = f.read()

start = fileContent.find(begin)
end = fileContent.find(end)

if start == -1 or end == -1:
    print('Nieprawidłowy klucz')
    exit

start = start + len(begin)

privkey = fileContent[start:end]
keyDecoded = b64decode(privkey)

print(RSA.importKey(keyDecoded, 'd').d)