import datetime as date
import sync
import hashlib
from block import Block


NUM_ZEROS = 5


def generate_header(index, prev_hash, data, timestamp, nonce):
    return str(index) + prev_hash + data + str(timestamp) + str(nonce)


def calculate_hash(index, prev_hash, data, timestamp, nonce):
    header_string = generate_header(index, prev_hash, data, timestamp, nonce)
    sha = hashlib.sha256()
    sha.update(header_string.encode())
    return sha.hexdigest()


def mine(last_block, data):
    index = int(last_block.index) + 1
    timestamp = date.datetime.now()
    # random string for now, not transactions
    # data = "I block #%s" % (int(last_block.index) + 1)
    prev_hash = last_block.hash
    nonce = 0

    block_hash = calculate_hash(index, prev_hash, data, timestamp, nonce)
    while str(block_hash[0:NUM_ZEROS]) != '0' * NUM_ZEROS:
        nonce += 1
        block_hash = calculate_hash(index, prev_hash, data, timestamp, nonce)

    # dictionary to create the new block object.
    block_data = {}
    block_data['index'] = index
    block_data['prev_hash'] = last_block.hash
    block_data['timestamp'] = timestamp
    block_data['data'] = data
    block_data['hash'] = block_hash
    block_data['nonce'] = nonce
    return Block(**block_data)


if __name__ == '__main__':
    data = "Un nuevo bloque"
    # gather last node
    node_blocks = sync.sync()
    prev_block = node_blocks[-1]
    # TODO aqui en [-1] no necesariamente agarra al último bloque, hay que \
    # ordenarlos antes
    new_block = mine(prev_block, data)
    new_block.self_save()
