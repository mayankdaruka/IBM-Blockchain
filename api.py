from flask import Flask, request
import requests
from blockchain import Blockchain
from block import Block
import time
import json

# Initialize flask application interface
app = Flask(__name__)

# Initialize blockchain object
blockchain = Blockchain()

@app.route('/')
def frontPage():
   return '''
   <html>
      <head>
            <title>Templating in Flask</title>
        </head>
        <body>
            <h1>Hello %s!</h1>
            <p>Welcome to the world of Flask!</p>
        </body>
   </html> ''' %"mayank"

# CENTRALIZED SO FAR

# Endpoint to submit a new unconfirmed transaction to the blockchain
@app.route("/newTransactions", methods=['POST'])
def newTransaction():
   transactionData = request.get_json()
   if ("author" not in transactionData or "content" not in transactionData):
      return "Invalid transaction data", 404
   
   transactionData["timestamp"] = time.time()
   blockchain.addUnconfirmedTransaction(transactionData)

   return "Success", 201

# Endpoint to retrieve and return a copy of the blockchain
@app.route('/blockchain', methods=['GET'])
def getBlockchain():
   blockArr = []
   for block in blockchain.chain:
      blockArr.append(block.__dict__)
   return json.dumps({ "length": len(blockArr), "chain": blockArr })

# Endpoint to request the node to mine the pending transaction
@app.route('/mineData', methods=['GET'])
def mineUnconfirmedTransactions():
   newBlockIndex = blockchain.mineData()
   if (not newBlockIndex):
      return "There are no transactions to mine"
   else:
      # Run consensus algorithm, make sure node has longest chain
      blockchainLen = len(blockchain.chain)
      consensusAlgorithm() # Update blockchain to longest valid chain if needed
      if (blockchainLen == len(blockchain.chain)):
         announceBlock(blockchain.chain[-1]) # CONFUSED: if running consensus(), what if chain is updated and we lose the mined block?
      return "Block " + str(newBlockIndex) + "has been mined!"

# Endpoint to retrieve all the pending unconfirmed transactions
@app.route('/pendingTransactions', methods=['GET'])
def getPendingTransactions():
   return json.dumps(blockchain.unconfirmedTransactions)


# MAKE NETWORK DECENTRALIZED, transition from a single node to a peer-to-peer network

# Contains host addresses of other members in network
peers = set()

# Endpoint to add new peers to network
@app.route('/registerNewNode', methods=['POST'])
def registerNewPeers():
   peerNodeAddress = request.get_json()['nodeAddress']
   if (not peerNodeAddress):
      return "Invalid data", 400
   peers.add(peerNodeAddress)
   # Return blockchain to new node for sync purposes
   return getBlockchain()

# Endpoint to register a new node with an existing node in the network
@app.route('/registerWithNode', methods=['POST'])
def registerWithExistingNode():
   newNodeAddress = request.get_json()['nodeAddress']
   if (not newNodeAddress):
      return "Invalid data", 400
   
   data = { "nodeAddress": request.host_url }
   headers = { "Content-Type": "application/json" }
   response = requests.post(newNodeAddress + "/registerNewNode", data=json.dumps(data), headers=headers)

   if (response.status_code == 200):
      # New node successfully registered
      # Update chain and peers
      global blockchain
      global peers
      chainBlockArr = response.json()['chain']
      peers.update(response.json['peers']) # peers field inside response.json() doesn't exist, so empty right now
      blockchain = createNewBlockchain(chainBlockArr)
      return "Registered node successfully", 200
   else:
      # Let codebase calling API figure it out
      return response.content, response.status_code

def createNewBlockchain(blockArr):
   blockchain = Blockchain()
   index = 0
   for blockData in blockArr:
      block = Block(blockData['index'], blockData['transactions'], blockData['timestamp'], blockData['prevHash'])
      hashProof = blockData['objHash']
      if (index > 0):
         # Verify added block along with difficulty of requirements
         addedBlock = blockchain.addBlock(block)
         if (not addedBlock):
            # Block not valid and cannot be added
            raise Exception("Chain is tampered.")
      else:
         # Genesis block, no need for verification
         blockchain.chain.append(block)
      index += 1
   return blockchain

# Endpoint to add block mined by someone else to current node's chain
@app.route('/addBlock', methods=['POST'])
def addNewBlock():
   blockData = request.get_json()
   newBlock = Block(blockData['index'], blockData['transactions'], blockData['timestamp'], blockData['prevHash'])
   hashProof = blockData['objHash']
   addedBlock = blockchain.addBlock(newBlock, hashProof)
   if (not addedBlock):
      return "Block couldn't be added to node's chain", 400
   return "Block successfully added", 201 # 201 status code == success and creation of new resource

"""
Announce to all nodes in the network that a block has
been mined. Adds the block to the chain for each node.
"""
def announceBlock(block):
   for nodeAddress in peers:
      requests.post(nodeAddress + "/addBlock", data=json.dumps(block.__dict__, sort_keys=True))

"""
Consensus algorithm to ensure consistency of chain among all nodes
in the network. Finds the longest valid chain and replaces current
blockchain with it.
"""
def consensusAlgorithm():
   global blockchain

   longestValidChain = None
   currentChainLen = 0

   for nodeAddress in peers:
      # Get the current node's copy of the blockchain
      response = request.get(str(nodeAddress) + "/blockchain")
      chainLen = response.get_json()['length']
      chain = response.get_json()['chain']
      if (chainLen > currentChainLen and blockchain.checkValidChain(chain)):
         currentChainLen = chainLen
         longestValidChain = chain

   if (longestValidChain):
      blockchain = longestValidChain
      return True
   return False


if (__name__ == "__main__"):
   app.run(debug=True, port=8000)