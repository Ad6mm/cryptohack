from Crypto.PublicKey import RSA

fileName = 'general/2048b-rsa-example-cert_3220bd92e30015fe4fbeb84a755e7ca5.der'

f = open(fileName, "rb")
fileContent = f.read()

key = RSA.importKey(fileContent)
print(key.n)
