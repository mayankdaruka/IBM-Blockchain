from Crypto.PublicKey import RSA
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

# publicKey = RSA.import_key(open("public.pem").read())
publicKey = RSA.import_key(open('public.pem').read())
privateKey = RSA.import_key(open('private.pem').read())

print(publicKey)
print(privateKey)

def signHashedTransaction(hashedTransaction):
   # fips-186-3 is one of four revisions to the Digital Signature Standard
   signer = DSS.new(privateKey, 'fips-186-3')
   signature = signer.sign(hashedTransaction)
   return signature

def verifyPost(hashedTransaction, signature):
   verifier = DSS.new(publicKey, 'fips-186-3')
   try:
      verifier.verify(hashedTransaction, signature)
      print("The post is authentic")
   except ValueError:
      print("The post is NOT authentic")