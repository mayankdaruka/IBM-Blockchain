from hashlib import sha256
import json

"""
Transaction JSON fields:
{
   "author" : "name of person who created post",
   "content" : "content of the post",
   "timestamp" : "time the post was created"
}
"""

class Block:
   """
   blockIndex: unique ID of the block
   transactionList: list of transactions that the block includes
   timeCreated: time that block was created
   prevHash: the hash of the previous block in the blockchain
   """
   def __init__(self, blockIndex, transactionList, timeCreated, previousHash):
      self.index = blockIndex
      self.transactions = transactionList
      self.timestamp = timeCreated
      self.prevHash = previousHash

   """
   Return hash of this block (SHA-256)
   """
   def computeHash(self):
      # Convert dictionary holding block properties into string
      blockStr = json.dumps(self.__dict__, sort_keys=True)
      return sha256(blockStr.encode()).hexdigest()
