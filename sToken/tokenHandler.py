from web3 import Web3, HTTPProvider, IPCProvider
import os
from os.path import basename, join
import json

web3 = Web3(HTTPProvider('http://localhost:8545'))
print(web3.eth.blockNumber)

class ContractHandler:
  def __init__(self):
    # self.web3 = Web3(RPCProvider(host='localhost', port='8545'))
    self.web3 = Web3(HTTPProvider('http://localhost:8545'))
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # load the json abi encoding for the contract
    with open(str(join(dir_path, 'tokeAbi.json')), 'r') as abi_definition:
      self.abi = json.load(abi_definition)
    # use the address of the contract you created with `truffle migrate --reset`
    self.token_address = '0x17a7f5449c236a998700bcdfeaeb2b3e1c346d1e'
    self.token = self.web3.eth.contract(self.abi, self.token_address)
    # check to see we have a valid contract object
    print(self.token)
    # check the total supply of this token contract with a call
    tSupply = self.token.call().totalSupply()
    print(tSupply)
    # use transact to send transactions that update state
    self.token.transact({'from': web3.eth.accounts[0]}).transfer(web3.eth.accounts[1], 1337)
    accountTwoBalance = self.token.call().balanceOf(web3.eth.accounts[1])
    # account two will now have a new balance after the block is confirmed
    # this will print 0 the first time you run it and 1337 the second
    print(accountTwoBalance)
handler = ContractHandler()
