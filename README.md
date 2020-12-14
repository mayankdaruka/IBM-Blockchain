# IBM-Blockchain
Implementing a blockchain using Python. Knowledge derived from "Bitcoin and Cryptocurrency Technologies" course taken on Coursera.
This is a decentralized content sharing system that I have implemented with a peer-to-peer network using Blockchain. Some additional features include a brute force
Proof-of-Work mining algorithm, a distributed consensus algorithm, block hashing with SHA-256, and RSA digital signatures to authenticate transactions.

I have created a simple web application with Flask to interface with the blockchain - it contains block mining, syncing, and content posting functionalities. You can also run
the application with multiple nodes by running it on different ports, to test out the functionalities of the peer-to-peer network.

The port 8000 is used to directly interface with the blockchain, allowing other nodes in the network to sync with the blockchain and mine blocks. The url specified for this is in api.py, and can be changed if needed.
