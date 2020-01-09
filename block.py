import hashlib
import json
import config


class Block():
    def __init__(self, **dictionary):
        '''
          We're looking for index, timestamp, data, prev_hash, nonce
        '''
        for key, value in dictionary.items():
            if key in config.BLOCK_VAR_CONVERSIONS:
                # FIX timestamp to be a string and then transformed to datetime
                setattr(self, key, config.BLOCK_VAR_CONVERSIONS[key](value))
                # TODO else, control what type of data to add
            elif key == "data":
                setattr(self, key, value)
        # in creating the first block, needs to be removed in future
        if not hasattr(self, 'hash'):
            self.hash = self.update_self_hash()

        if not hasattr(self, 'nonce'):
            # we're throwin this in for generation
            self.nonce = 'None'

    def header_string(self):
        return str(self.index) + self.prev_hash + self.data +\
                str(self.timestamp) + str(self.nonce)

    def generate_header(index, prev_hash, data, timestamp, nonce):
        # FIX if data not just a string, hash data first
        header = str(index) + prev_hash + data + str(timestamp) + str(nonce)
        return header

    def update_self_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.header_string()).encode())
        new_hash = sha.hexdigest()
        self.hash = new_hash
        # print(f"Hash del nuevo bloque: {new_hash}\n")
        return new_hash

    def self_save(self):
        # front of zeros so they stay in numerical order
        index_string = str(self.index).zfill(6)
        filename = '%s%s.json' % (config.CHAINDATA_DIR, index_string)
        with open(filename, 'w') as block_file:
            json.dump(self.to_dict(), block_file)

    def to_dict(self):
        info = {}
        info['index'] = str(self.index)
        info['timestamp'] = str(self.timestamp)
        info['prev_hash'] = str(self.prev_hash)
        info['hash'] = str(self.hash)
        info['data'] = str(self.data)
        info['nonce'] = str(self.nonce)
        return info

    def is_valid(self):
        self.update_self_hash()
        if str(self.hash[0:config.NUM_ZEROS]) == ('0' * config.NUM_ZEROS):
            return True
        else:
            return False

    def __repr__(self):
        return "Block <index: %s>, <hash: %s>" % (self.index, self.hash)

    def __eq__(self, other):
        return (self.index == other.index and
                self.timestamp == other.timestamp and
                self.prev_hash == other.prev_hash and
                self.hash == other.hash and
                self.data == other.data and
                self.nonce == other.nonce)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return self.timestamp < other.timestamp

    def __lt__(self, other):
        return self.timestamp > other.timestamp
