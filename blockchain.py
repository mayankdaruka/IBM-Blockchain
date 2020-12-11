import time
from block import Block

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

   """
   Adds a block to the blockchain after its validity
   has been verified
   """
   def addBlock(self, newBlock, hashProof):
      lastBlock = self.chain[-1]
      
      if (newBlock.prevHash != lastBlock.objHash):
         return False
      if (not validBlock(newBlock, hashProof)):
         return False

      newBlock.hash = hashProof
      self.chain.append(newBlock)
      return True


   """
   Checks if the hash of the block is valid and
   satisifies the difficulty requirements
   """
   def validBlock(self, block, blockHash):
      return (blockHash.startsWith('0'*difficulty) and block_hash == block.computeHash())

chain = Blockchain()
chain.createGenesisBlock()