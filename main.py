import datetime
from block import Block
from chain import Chain

'''
We're looking for index, timestamp, data, prev_hash, nonce
'''

block1 = {"index": 1, "data": "hola 1", "timestamp": datetime.datetime.now().strftime('%s')}
block1 = {"index": 2, "data": "hola 1", "timestamp": datetime.datetime.now().strftime('%s')}
block1 = {"index": 3, "data": "hola 1", "timestamp": datetime.datetime.now().strftime('%s')}
block1 = {"index": 4, "data": "hola 1", "timestamp": datetime.datetime.now().strftime('%s')}


if __name__ == "__main__":
    BC = Chain([])


