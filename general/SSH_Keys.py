from Crypto.PublicKey import RSA

fileName = 'general/bruce_rsa_6e7ecd53b443a97013397b1a1ea30e14.pub'

f = open(fileName, "r")
fileContent = f.read()

key = RSA.importKey(fileContent)
print(key.n)