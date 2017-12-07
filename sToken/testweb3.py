from web3 import Web3, HTTPProvider, IPCProvider

# simple HTTP connection and print block
web3 = Web3(HTTPProvider('http://localhost:8545'))
block = web3.eth.blockNumber
print(block)