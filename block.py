from hashlib import sha256
import json

class Block:
   """
   blockIndex: unique ID of the block
   transactionList: list of transactions that the block includes
   timeCreated: time that block was created
   prevHash: the hash of the previous block in the blockchain
   """
   def __init__(self, blockIndex, transactionList, timeCreated, prevHash):
      self.index = blockIndex
      self.transactions = transactionList
      self.timestamp = timeCreated
      print(self.__dict__)


   """
   Return hash of this block (SHA-256)
   """
   def computeHash(self):
      # Convert dictionary holding block properties into string
      blockStr = json.dumps(self.__dict__, sort_keys=True)
      return sha256(blockStr.encode()).hexdigest()

block = Block(1, 2, 4, "0")
print(block.computeHash())
