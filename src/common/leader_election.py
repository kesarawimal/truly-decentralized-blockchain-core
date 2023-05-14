import json
import random
from src.common.io_mem_pool import get_transactions_from_memory
from src.common.io_voting import get_voting_from_memory
from src.common.new_user_creation import get_key_pair_from_memory


def random_leader_election(network):
    transactions = get_transactions_from_memory()
    transaction = random.choice(transactions)
    voting = {
        "voter_hex": json.loads(get_key_pair_from_memory())["public key hex"],
        "voting_hex": transaction['inputs'][0]['unlocking_script'].split(' ')[1]
    }
    broadcast(voting, network)


def broadcast(voting, network):
    node_list = network.known_nodes
    for node in node_list:
        if node.hostname != network.node.hostname:
            node.send_voting(voting)


def get_current_votes():
    voting = get_voting_from_memory()
    count = 0
    for vote in voting:
        if vote['voting_hex'] == json.loads(get_key_pair_from_memory())["public key hex"]:
            count = count + 1
    return count
