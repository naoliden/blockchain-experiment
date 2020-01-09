import config


def is_valid_chain(blockchain):
    '''
      We need to check to see if the entire chain is valid.
      To do this, we check if each block in order is valid.
      The is_valid() function in the Block class handles the
      hash connection between the previous and current block.
    '''
    for b in blockchain:
        if not b.is_valid():
            return False
    return True


def dict_from_block_attributes(**kwargs):
    info = {}
    for key in kwargs:
        if key in config.BLOCK_VAR_CONVERSIONS:
            info[key] = config.BLOCK_VAR_CONVERSIONS[key](kwargs[key])
        else:
            info[key] = kwargs[key]
    return info
