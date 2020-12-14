from Crypto.PublicKey import RSA
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from store_keys import key
from Crypto.Hash import SHA256

publicKey = RSA.import_key(open('public.pem', 'r').read())
privateKey = RSA.import_key(open('private.pem', 'r').read())

print(publicKey)
print(privateKey)

def signHashedTransaction(hashedTransaction, keyPair):
   # fips-186-3 is one of four revisions to the Digital Signature Standard
   # signer = DSS.new(privateKey, 'fips-186-3')
   msg = b'Message for RSA signing'
   hash = SHA256.new(msg)
   signer = PKCS115_SigScheme(keyPair)
   signature = signer.sign(hash)
   return signature

def verifyPost(hashedTransaction, signature, publicKey):
   # verifier = DSS.new(publicKey, 'fips-186-3')
   verifier = PKCS115_SigScheme(publicKey)
   msg = b'Message for RSA signing'
   hash = SHA256.new(msg)
   try:
      verifier.verify(hash, signature)
      print("The post is authentic")
   except ValueError:
      print("The post is NOT authentic")

signature = signHashedTransaction("008ff6ebd154c76a50058b53ea4cd18807b5d729c67314585e824d801793fed5", key)
print(signature)
verifyPost("sdf", signature, publicKey)