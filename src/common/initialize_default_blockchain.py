from datetime import datetime
import json

from common.io_blockchain import store_blockchain_in_memory
from common.new_user_creation import get_key_pair_from_memory
from common.block import Block, BlockHeader
from common.merkle_tree import get_merkle_root
from common.transaction import Transaction
from common.transaction_input import TransactionInput
from common.transaction_output import TransactionOutput


def initialize_default_blockchain():
    print("Initializing default blockchain")
    timestamp_0 = datetime.timestamp(datetime.fromisoformat('2011-11-04 00:05:23.111'))
    input_0 = TransactionInput(transaction_hash="0000000000000000000000000000000000000000000000000000000000000000",
                               output_index=0)
    output_0 = TransactionOutput(public_key_hash=json.loads(get_key_pair_from_memory())['public key hash'], amount=50)
    transaction_0 = Transaction([input_0], [output_0])
    block_header_0 = BlockHeader(previous_block_hash="0000000000000000000000000000000000000000000000000000000000000000",
                                 timestamp=timestamp_0,
                                 nonce=00000,
                                 merkle_root=get_merkle_root([transaction_0.transaction_data]))
    block_0 = Block(
        block_header=block_header_0,
        transactions=[transaction_0.transaction_data]
    )
    store_blockchain_in_memory(block_0)
