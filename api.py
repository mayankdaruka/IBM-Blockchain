from flask import Flask, request
import requests
from blockchain import Blockchain

# Initialize flask application interface
app = Flask(__name__)

# Initialize blockchain object
blockchain = Blockchain()