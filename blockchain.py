from hashlib import sha256
import time
import sys
import pickle
import os.path

#Block class t0 create new blocks for the blockchain
class block:
    def __init__(self, index, timeStamp, blockData, previousHash, currentHash):
        self.index = index
        self.timeStamp = timeStamp
        self.blockData = blockData
        self.previousHash = previousHash
        self.currentHash = currentHash

#The genesis block of the blockchain
def genesisBlock():
    genesis_block = block(0, 1518880729.6806366, "I am the genesis block", "0", "2cf876b736eb087dfbfe68f85adf1b2e2f5f016f5b69e56e372cff0d82cfb36d")
    return genesis_block

#Get the last block of the blockchain
def getLastBlock():
    return(blockchain[len(blockchain)-1])

#hash the block
def hashData (index, timeStamp, blockData, previousHash):
    data = str(index) + str(timeStamp) + str(blockData) + str(previousHash)
    data = data.encode('utf-8')
    return sha256(data).hexdigest()

#create a new block for the blockchain
def createNewBlock(data):
    previousBlock = getLastBlock()
    nextIndex = previousBlock.index + 1
    nextTimeStamp = time.time()
    nextHash = hashData(nextIndex, nextTimeStamp, data, previousBlock.blockData)
    nextBlock = block(nextIndex, nextTimeStamp, data, previousBlock.currentHash, nextHash)
    return nextBlock

#add a created block to the blockchain
def addNextBlockToBlockchain(newBlock):
    if(checkValidity(newBlock, getLastBlock())):
        blockchain.append(newBlock)

#check the validity of the block and the last block
def checkValidity(newBlock, lastBlock):
    if(newBlock.previousHash != lastBlock.currentHash):
        return False
    return True

def main():
  blockchain.append(genesisBlock())

if __name__== "__main__":
  blockchain = []
  try:
      read_file = open("blockchain.bl", 'rb')
  except IOError:
      print("Error opening the blockchain")

  if os.path.exists("blockchain.bl"):
      blockchain = pickle.load(read_file)
  else:
      write_file = open("blockchain.bl", 'wb')
      main()
    #call main funciton to add the genesis block

  while True:
      user_input = input("Add block to blockchain by typing your data or show to show the blockchain: ")
      #show the whole blockchain
      if user_input == "show":
          for a in blockchain:
              print(str(a.index) + ": " + a.blockData)
              print(str(a.currentHash)+"\n")
      #exit the script
      elif user_input == "exit":
          write_file = open("blockchain.bl", 'wb')
          pickle.dump(blockchain, write_file)
          sys.exit("Stopped by user input")
      #add a new block to the blockchain
      else:
          addNextBlockToBlockchain(createNewBlock(user_input))
