from web3 import Web3, HTTPProvider, IPCProvider
import os
from os.path import basename, join
import json
from time import sleep

token_address = '0x243eb4baabd87606e9d4a121c26ea8c3db79e847'
contract2_address = '0x6a622c7ca41fe910989a9313ded9e2b202da4a1a'

totalSupply = 66363636600000000

def callback(res):
  # the response is an event object that will contain the args logged
  print(res)


class ContractHandler:
  def __init__(self):
    # self.web3 = Web3(RPCProvider(host='localhost', port='8545'))
    self.web3 = Web3(HTTPProvider('http://localhost:8545'))
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # load the json abi encoding for the contract
    with open(str(join(dir_path, 'contractTwoAbi.json')), 'r') as abi_definition:
      self.abi = json.load(abi_definition)

    # use the address of the contract you created with `truffle migrate --reset`
    self.contract2 = self.web3.eth.contract(self.abi, contract2_address)

    # sleep for the transaction to be mined and the callback to be fired
    oracle = self.contract2.call().oracles(self.web3.eth.accounts[2])
    # Should print the address of account 1 if the oracle was registered
    print('Miner registration: ', oracle[0])


    # The owner can set the miners/devs of the attribution rewards
    # The tx must be sent from account 0 - owner account of the deployed contract
    # This sets account 1 as an oracle for mining
    if oracle[0] == '0x0000000000000000000000000000000000000000':
      self.contract2.transact().addOracle(self.web3.eth.accounts[2], 'testname')

    # create an event filter and listen for the add oracle event
    oracleFilter = self.contract2.on('OracleAdded')
    oracleFilter.watch(callback)

    # sleep for the transaction to be mined and the callback to be fired
    sleep(5)
    oracle = self.contract2.call().oracles(self.web3.eth.accounts[2])
    # Should print the address of account 1 if the oracle was registered
    print('Miner registration: ', oracle)

    # now that an oracle is added approve tokens to the mining supply
    # load the json abi encoding for the contract
    with open(str(join(dir_path, 'tokenAbi.json')), 'r') as abi_definition:
      self.abi_token = json.load(abi_definition)
    self.token = self.web3.eth.contract(self.abi_token, token_address)

    isActive = self.contract2.call().activated()
    if not isActive:
      # approve contract the ability to send tokens on owners behalf
      self.token.transact({'from': self.web3.eth.accounts[0]}).approve(contract2_address, totalSupply)

      # check the approval
      sleep(3)
      allow = self.token.call().allowance(self.web3.eth.accounts[0], contract2_address)
      print('Contract 2 ready to call genesis with :',allow, ' tokens')

      # start the mining process by calling the genesis function
      self.contract2.transact({'from': self.web3.eth.accounts[0]}).genesis()
      sleep(3)
      isActive = self.contract2.call().activated()
      print('Contract 2 ready to mine: ', isActive)

    # mine the first block
    print('---------------------------------')
    data_location = '-----BEGIN PGP MESSAGE-----\nVersion: Keybase OpenPGP v2.0.76\n Comment: https://keybase.io/crypto\n\nwcBMA+Z2g4bI5kpsAQf/TstGHcXuqNaYShJNXtn6JAIwFlD+8mCWbG+0RigpU94V\nbQ8+gzpghti5pNaJbPacK3xKkEpQ0qSWHCI2IOjzplsYDtDcA0XdZoAOiHe+IWJp\nB+tayXz9K60+fHFDw/idnld2vb1FGK60O9KwB3Xg+6X103yfmiX9qqWn9UMvVmJs\nitg7iJZGFDS8687V1+x8Cbq19ww1NsBie93iVJISLkDELtYeHs05JgI0b/fKxBbF\n0gXiEjrLppT5owNySdazKadSZsFzkn8M4GqpOTPPGWylZW32CRKHNFx50CvDBDWb\nW9l7bRQ+JJABLmD4hw95Q96rMGh4lhkk5MbKNpGdkdJWAbYmWnaZOG5Jandunbk2\nM8ZCPMnSycrqgNXGyuijg2sIoh+HxR3t/BOmPtHLJOjdfQhXu02QoMUmJQlfYR31\ndO0eY0WnY6hKqRng4RHESWWzAajGp1E==IZPF\n-----END PGP MESSAGE-----\n'
    # data_location = 'test'
    self.contract2.transact({'from': self.web3.eth.accounts[2], 'gas': 2500000}).mineBlock(data_location, self.web3.eth.accounts[1])
    blockFilter = self.contract2.on('BlockMined')
    blockFilter.watch(callback)

    sleep(5)
    height = self.contract2.call().blockHeight()
    print('Current block height: ', height)

    block = self.contract2.call().blockChain(height)
    print('Current block: ', block)

    #check that the balance was provided to the miner
    miner_balance = self.token.call().balanceOf(self.web3.eth.accounts[2])
    print('Balance of miner: ', miner_balance)

    #check that the balance was provided to the provider
    p_balance = self.token.call().balanceOf(self.web3.eth.accounts[1])
    print('Balance of provider: ', p_balance)

handler = ContractHandler()
