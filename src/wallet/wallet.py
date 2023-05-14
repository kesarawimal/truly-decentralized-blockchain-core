import requests

from src.common.transaction import Transaction
from src.common.transaction_input import TransactionInput
from src.common.transaction_output import TransactionOutput
from src.common.owner import Owner


class Wallet:
    def __init__(self, owner: Owner, network):
        self.owner = owner
        self.network = network

    def process_transaction(self, inputs: [TransactionInput], outputs: [TransactionOutput]) -> requests.Response:
        transaction = Transaction(inputs, outputs)
        transaction.sign(self.owner)
        self.broadcast(transaction.transaction_data)

    def broadcast(self, transaction_data):
        node_list = self.network.known_nodes
        for node in node_list:
            if node.hostname != self.network.node.hostname:
                node.send_transaction(transaction_data)
