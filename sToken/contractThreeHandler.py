from web3 import Web3, HTTPProvider, IPCProvider
import os
from os.path import basename, join
import json
from time import sleep

token_address = '0x243eb4baabd87606e9d4a121c26ea8c3db79e847'
c3_address = '0x12e8e1891b66e2ad113ac411bcac37f2a1ddf7b0'

def callback(res):
  # the response is an event object that will contain the args logged
  print(res)


class ContractHandler:
  def __init__(self):
    # self.web3 = Web3(RPCProvider(host='localhost', port='8545'))
    self.web3 = Web3(HTTPProvider('http://localhost:8545'))
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # load the json abi encoding for the contract
    with open(str(join(dir_path, 'contractThreeAbi.json')), 'r') as abi_definition:
      self.abi = json.load(abi_definition)
    with open(str(join(dir_path, 'tokenAbi.json')), 'r') as abi_definition:
      self.abi_token = json.load(abi_definition)

    # use the address of the contract you created with `truffle migrate --reset`
    self.contract3 = self.web3.eth.contract(self.abi, c3_address)
    self.token = self.web3.eth.contract(self.abi_token, token_address)

    # Can make a request for data
    req = 'github, go-lang, python'
    cb = 'https://myDomain.com/where/to/send/purchased/data'
    self.contract3.transact({'from': self.web3.eth.accounts[1]}).addRequest(req, cb)
    # watch for the request event
    requestFilter = self.contract3.on('Request')
    requestFilter.watch(callback)
    sleep(3)
    reqCount = self.contract3.call().requestCount()
    print('Request Count: ', reqCount)
    tx = self.contract3.call().txs(self.web3.eth.accounts[1])
    print('Recorded TX: ', tx)

    # get open offers
    offer = self.contract3.call({'from': self.web3.eth.accounts[1]}).getOffer(0)
    print('Open offers: ', offer)

    # Create an offer
    self.contract3.transact({'from': self.web3.eth.accounts[0]}).processRequest(self.web3.eth.accounts[1], 1337)
    sleep(3)
    offer = self.contract3.call({'from': self.web3.eth.accounts[1]}).getOffer(1)
    print('Open offers: ', offer)

    # accept the offer and pay tokens
    # first the buyer must approve contract 3 to take the tokens
    print('Approving funds to contract 3...')
    self.token.transact().transfer(self.web3.eth.accounts[1], 1337)
    sleep(3)
    self.token.transact({'from': self.web3.eth.accounts[1]}).approve(c3_address, 1337)
    sleep(3)
    allow = self.token.call().allowance(self.web3.eth.accounts[1], c3_address)
    print('Contract 3 is approved: ', allow, ' SENSE')

    # call the confirm function to confirm the offer
    self.contract3.transact({'from': self.web3.eth.accounts[1]}).confirmOffer(1)
    sleep(3)

    tx = self.contract3.call().txs(self.web3.eth.accounts[1])
    print('Updated TX: ', tx)

    agent = self.contract3.call().agent()
    print('Agent: ', agent)

    agentBal = self.token.call().balanceOf(agent)
    print('Agent Balance: ', agentBal)

handler = ContractHandler()
