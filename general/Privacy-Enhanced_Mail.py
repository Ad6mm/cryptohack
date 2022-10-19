from Crypto.PublicKey import RSA
fileName = 'privacy_enhanced_mail_1f696c053d76a78c2c531bb013a92d4a.pem'

f = open("fileName", "r")
print(RSA.importKey(f.read()))