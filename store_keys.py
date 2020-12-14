from Crypto.PublicKey import RSA

key = RSA.generate(bits=1024)
privateKey = key.export_key('PEM')
publicKey = key.publickey().export_key('PEM')

# print("private key")
# print(privateKey)
# print("public key")
# print(publicKey)

writeKey = open("private.pem", "wb")
writeKey.write(privateKey)
writeKey.close()

writeKey = open("public.pem", "wb")
writeKey.write(publicKey)
writeKey.close()