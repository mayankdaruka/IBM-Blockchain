import time
from block import Block
from signature import signHashedTransaction, verifyPost
import binascii
import json
from Crypto.Hash import SHA256

class Blockchain:
   # difficult of the Proof of Work algorithm (number of zeroes)
   difficulty = 2

   """
   Creates and initialized a blockchain
   """
   def __init__(self):
      self.chain = []
      self.unconfirmedTransactions = []
      self.createGenesisBlock()

   """
   Creates the first block in the blockchain called
   a genesis block (has no previous hash)
   """
   def createGenesisBlock(self):
      genesisBlock = Block(0, [], time.time(), "0")
      genesisBlock.objHash = genesisBlock.computeHash()
      self.chain.append(genesisBlock)

   """
   Uses brute force to compute value of nonce that
   results in a hash satisfying the constraints
   """
   def proofOfWork(self, block):
      block.nonce = 0

      currHash = block.computeHash()

      # Keep finding value until constraints satisfied
      while (not currHash.startswith("0"*Blockchain.difficulty)):
         block.nonce += 1
         currHash = block.computeHash()

      return currHash

   """
   Adds a block to the blockchain after its validity
   has been verified
   """
   def addBlock(self, newBlock, hashProof):
      lastBlock = self.chain[-1]
      
      # Checks to make sure hash pointer points to previous block
      # and satisfies the difficulty criteria
      if (newBlock.prevHash != lastBlock.objHash):
         return False
      if (not self.validBlock(newBlock, hashProof)):
         return False

      # # Adds digital signature of transaction to object after hash calculated
      # newBlock.signature = signHashedTransaction(newBlock.getHashObj())
      # Adds objHash attribute after hash and signature calculated, so hash doesn't include objHash and signature values
      newBlock.objHash = hashProof
      self.chain.append(newBlock)
      return True


   """
   Checks if the hash of the block is valid and
   satisifies the difficulty requirements
   """
   def validBlock(self, block, blockHash):
      return (blockHash.startswith('0'*Blockchain.difficulty) and blockHash == block.computeHash())


   """
   Adds a transaction to a list of pending transactions
   that haven't been accounted for by the blockchain yet
   """
   def addUnconfirmedTransaction(self, newTransaction):
      self.unconfirmedTransactions.append(newTransaction)

   """
   Adds pending transactions to a block and adds block to
   the blockchain if everything is valid
   """
   def mineData(self):
      # No need to mine if nothing to add to blockchain
      if (not self.unconfirmedTransactions):
         return False

      finalTransactions = []
      for transaction in self.unconfirmedTransactions:
         signature = transaction['signature']
         del transaction['signature']
         if (verifyPost(SHA256.new(json.dumps(transaction).encode()), binascii.unhexlify(signature.encode('utf-8')))):
            finalTransactions.append(transaction)
         else:
            print("TRANSACTION NOT VALID")

      lastBlock = self.chain[-1]
      newBlock = Block(lastBlock.index + 1, finalTransactions, time.time(), lastBlock.objHash)

      finalHash = self.proofOfWork(newBlock)
      # Add block to blockchain once mining over (additional checks inside method)
      self.addBlock(newBlock, finalHash)
      # Done adding all pending transactions into a block, so empty list
      self.unconfirmedTransactions = []
      return newBlock.index

   """
   Checks if chain is valid
   """
   def checkValidChain(self, chain):
      valid = True
      prevHash = "0"
      
      for block in chain:
         blockHash = block.objHash
         # Delete objHash attribute to compute block's hash
         delattr(blockHash, 'objHash')

         if (not self.validBlock(block, blockHash) or prevHash != block.prevHash):
            valid = False
            break
         # Reassign attribute to block
         block.objHash = blockHash
         prevHash = blockHash
         
      return valid

# chain = Blockchain()
# chain.createGenesisBlock()