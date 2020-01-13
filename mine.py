import datetime
import sync
from block import Block
import config
import utils


def mine_for_block():
    print("mine for block sync")
    current_chain = sync.sync_local()  # gather last node
    print("mine for block sync done")
    prev_block = current_chain.most_recent_block()
    new_block = mine_blocks(prev_block)
    new_block.self_save()
    return new_block


def mine_blocks(last_block):
    index = int(last_block.index) + 1
    timestamp = datetime.datetime.now().strftime('%s')
    # random string for now, not transactions
    data = f"I block {int(last_block.index) + 1}"
    prev_hash = last_block.hash
    nonce = 0

    block_info_dict = utils.dict_from_block_attributes(index=index,
                                                       timestamp=timestamp,
                                                       data=data,
                                                       prev_hash=prev_hash,
                                                       nonce=nonce)
    new_block = Block(**block_info_dict)
    valid_block = find_valid_nonce(new_block)
    return valid_block


def find_valid_nonce(new_block):
    print(f"mining for block {new_block.index}")
    # calculate_hash(index, prev_hash, data, timestamp, nonce)
    new_block.update_self_hash()
    t1 = datetime.datetime.now()
    while str(new_block.hash[0:config.NUM_ZEROS]) != '0' * config.NUM_ZEROS:
        new_block.nonce += 1
        new_block.update_self_hash()
    t2 = datetime.datetime.now()
    print(f"block {new_block.index} mined. Nonce: {new_block.nonce}, time taken: {t2 - t1}")

    assert new_block.is_valid()
    return new_block  # we mined the block. We're going to want to save it

    # return True


if __name__ == '__main__':
    mine_for_block()
