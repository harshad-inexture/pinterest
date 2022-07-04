def block_user_list(blocks):
    block_list = []
    for block in blocks:
        block_list.append(block.user_id)
    return block_list
