import json
from datetime import datetime

from src.common.block import Block, BlockHeader
from src.common.io_blockchain import get_blockchain_from_memory
from src.common.io_mem_pool import get_transactions_from_memory
from src.common.merkle_tree import get_merkle_root
from src.common.network import Network
from src.common.utils import calculate_hash
from src.common.values import NUMBER_OF_LEADING_ZEROS


class BlockException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class ProofOfWork:
    def __init__(self, network: Network):
        self.network = network
        self.blockchain = get_blockchain_from_memory()
        self.new_block = None

    @staticmethod
    def get_nonce(block_header: BlockHeader) -> int:
        block_header_hash = ""
        nonce = block_header.nonce
        starting_zeros = "".join([str(0) for _ in range(NUMBER_OF_LEADING_ZEROS)])
        while not block_header_hash.startswith(starting_zeros):
            nonce = nonce + 1
            block_header_content = {
                "previous_block_hash": block_header.previous_block_hash,
                "merkle_root": block_header.merkle_root,
                "timestamp": block_header.timestamp,
                "nonce": nonce,
                "complexity": block_header.complexity
            }
            block_header_hash = calculate_hash(json.dumps(block_header_content))
        return nonce

    def create_new_block(self):
        transactions = get_transactions_from_memory()
        if transactions:
            block_header = BlockHeader(
                merkle_root=get_merkle_root(transactions),
                previous_block_hash=self.blockchain.block_header.hash,
                timestamp=datetime.timestamp(datetime.now()),
                nonce=0,
                complexity=self.blockchain.get_complexity()
            )
            block_header.nonce = self.get_nonce(block_header)
            block_header.hash = block_header.get_hash()
            self.new_block = Block(transactions=transactions, block_header=block_header)
            print("A new block has been successfully forged.")
        else:
            raise BlockException("", "No transaction in mem_pool")

    def broadcast(self):
        node_list = self.network.known_nodes
        for node in node_list:
            if node.hostname != self.network.node.hostname:
                block_content = {
                    "block": {
                        "header": self.new_block.block_header.to_dict,
                        "transactions": self.new_block.transactions
                    }
                }
                node.send_new_block(block_content)
