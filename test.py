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
    with open(str(join(dir_path, 'abi.json')), 'r') as abi_definition:
      self.abi = json.load(abi_definition)
    self.contract_address = '0x97CA8108064eB2a90428ED6f407AE583eE7C3fd8'
    self.contract = self.web3.eth.contract(self.abi, self.contract_address)
    print(self.contract)

handler = ContractHandler()