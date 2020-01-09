import hashlib
import os
import json
from datetime import datetime


class Block():
    def __init__(self, **dictionary):
        '''
        We're looking for index, timestamp, data, prev_hash, nonce
        '''
        for key, value in dictionary.items():
            setattr(self, key, value)
        if not hasattr(self, 'nonce'):
            # we're throwin this in for generation
            self.nonce = 'None'
        if not hasattr(self, 'hash'):
            # in creating the first block, needs to
            # be removed in future
            self.hash = self.create_self_hash()

    def header_string(self):
        result = str(self.index) + self.prev_hash + self.data + \
            str(self.timestamp) + str(self.nonce)
        return result.encode()

    def create_self_hash(self):
        sha = hashlib.sha256()
        sha.update(self.header_string())
        result_hash = sha.hexdigest()
        print(f"Hash del nuevo bloque: {result_hash}\n")
        return result_hash

    def self_save(self):
        chaindata_dir = 'chaindata'
        index_string = str(self.index).zfill(6)
        # front of zeros so they stay in numerical order
        filename = f"{chaindata_dir}/{index_string}.json"
        with open(filename, 'w') as block_file:
            json.dump(self.__dict__(), block_file)

    def __dict__(self):
        info = {}
        info['index'] = str(self.index)
        info['timestamp'] = str(self.timestamp)
        info['prev_hash'] = str(self.prev_hash)
        info['hash'] = str(self.hash)
        info['data'] = str(self.data)
        info['nonce'] = str(self.nonce)
        return info

    def __str__(self):
        return f"Block <prev_hash: {self.prev_hash}, hash: {self.hash} >"


def create_first_block():
    # index zero and arbitrary previous hash
    block_data = {}
    block_data['index'] = 0
    block_data['timestamp'] = datetime.now()
    block_data['data'] = 'First block data'
    block_data['prev_hash'] = ''
    # starting it at 0
    block_data['nonce'] = 0
    return Block(**block_data)


if __name__ == '__main__':
    # check if chaindata folder exists.
    chaindata_dir = 'chaindata/'
    if not os.path.exists(chaindata_dir):
        # make chaindata dir
        os.mkdir(chaindata_dir)
    # check if dir is empty from just creation, or empty before
    if os.listdir(chaindata_dir) == []:
        # create and save first block
        first_block = create_first_block()
        first_block.self_save()
