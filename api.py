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
   if (not newBlockIndex)
      return "There are no transactions to mine"
   return "Block " + str(newBlockIndex) + "has been mined!"

# Endpoint to retrieve all the pending unconfirmed transactions
@app.route('/pendingTransactions', methods=['GET'])
def getPendingTransactions():
   return json.dumps(blockchain.unconfirmedTransactions)


# MAKE NETWORK DECENTRALIZED
# Transition from a single node to a peer-to-peer network

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
      blockchain = createNewBlockchain(chainBlockArr)

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
