from Crypto.PublicKey import RSA
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from store_keys import key
from Crypto.Hash import SHA256
from block import block
import binascii

publicKey = RSA.import_key(open('public.pem', 'r').read())
privateKey = RSA.import_key(open('private.pem', 'r').read())

print(publicKey)
print(privateKey)

def signHashedTransaction(hashedTransaction):
   signer = PKCS115_SigScheme(key)
   signature = signer.sign(hashedTransaction)
   # return tuple for signature
   return (binascii.hexlify(signature).decode('utf-8'), signature)

def verifyPost(hashedTransaction, signature, publicKey):
   # verifier = DSS.new(publicKey, 'fips-186-3')
   verifier = PKCS115_SigScheme(publicKey)
   try:
      verifier.verify(hashedTransaction, signature)
      print("The post is authentic")
   except ValueError:
      print("The post is NOT authentic")

signature = signHashedTransaction(block.getHashObj())[1]
print(signature)
verifyPost(block.getHashObj(), signature, publicKey)