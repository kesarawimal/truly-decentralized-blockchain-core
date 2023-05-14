import json
from flask import Flask, request, jsonify, render_template
from src.common.io_mem_pool import get_transactions_from_memory
from src.common.io_voting import store_voting_in_memory
from src.common.transaction_input import TransactionInput
from src.common.transaction_output import TransactionOutput
from src.common.io_blockchain import get_blockchain_from_memory
from src.common.network import Network
from src.common.node import Node
from src.common.new_user_creation import get_key_pair_from_memory
from src.node.new_block_creation.new_block_creation import ProofOfWork
from src.node.new_block_validation.new_block_validation import NewBlock, NewBlockException
from src.node.transaction_validation.transaction_validation import Transaction, TransactionException
from src.wallet.wallet import Wallet
from src.doc.private_key import private_key
from src.common.owner import Owner
from src.common.leader_election import random_leader_election, get_current_votes

app = Flask(__name__)

MY_HOSTNAME = "127.0.0.1:5000"
my_node = Node(MY_HOSTNAME)
network = Network(my_node)
network.join_network()


@app.route("/block", methods=['GET', 'POST'])
def validate_block():
    blockchain_base = get_blockchain_from_memory()
    if request.method == 'POST':
        content = request.json
        try:
            block = NewBlock(blockchain_base, network)
            block.receive(new_block=content["block"])
            block.validate()
            block.add()
            block.broadcast()
            block.sanitize()
        except (NewBlockException, TransactionException) as new_block_exception:
            return f'{new_block_exception}', 400
        return "Transaction success", 200
    else:
        return jsonify(blockchain_base.to_dict)


@app.route("/transactions", methods=['POST'])
def validate_transaction():
    content = request.json
    blockchain_base = get_blockchain_from_memory()
    try:
        transaction = Transaction(blockchain_base, network)
        transaction.receive(transaction=content)
        if transaction.is_new:
            transaction.validate()
            transaction.validate_transaction_hash()
            transaction.validate_funds()
            transaction.store()
            transaction.broadcast()
    except TransactionException as transaction_exception:
        return f'{transaction_exception}', 400
    if len(get_transactions_from_memory()) == blockchain_base.get_complexity():
        random_leader_election(network)
    return "Transaction success", 200


@app.route("/voting", methods=['POST'])
def get_voting():
    content = request.json
    try:
        store_voting_in_memory(content)
        if get_current_votes() >= (get_blockchain_from_memory().get_complexity() / 2):
            pow = ProofOfWork(network)
            pow.create_new_block()
            pow.broadcast()
    except:
        return f'voting error', 400
    return "Voting success", 200


@app.route("/election", methods=['GET'])
def election():
    random_leader_election(network)


@app.route("/blockchain", methods=['GET'])
def get_blocks():
    blockchain_base = get_blockchain_from_memory()
    return render_template('blockchain.html', blockchain=blockchain_base.to_dict)


@app.route("/blockchain/raw", methods=['GET'])
def get_raw_blocks():
    blockchain_base = get_blockchain_from_memory()
    return jsonify(blockchain_base.to_dict)


@app.route("/utxo/<user>", methods=['GET'])
def get_user_utxos(user):
    blockchain_base = get_blockchain_from_memory()
    return jsonify(blockchain_base.get_user_utxos(user))


@app.route("/transactions/<transaction_hash>", methods=['GET'])
def get_transaction(transaction_hash):
    blockchain_base = get_blockchain_from_memory()
    return jsonify(blockchain_base.get_transaction(transaction_hash))


@app.route("/new_node_advertisement", methods=['POST'])
def new_node_advertisement():
    content = request.json
    hostname = content["hostname"]
    try:
        new_node = Node(hostname)
        network.store_new_node(new_node)
    except TransactionException as transaction_exception:
        return f'{transaction_exception}', 400
    return "New node advertisement success", 200


@app.route("/known_node_request", methods=['GET'])
def known_node_request():
    return jsonify(network.return_known_nodes())


@app.route("/peer", methods=['GET', 'POST'])
def peer():
    peers = network.return_known_nodes()
    if request.method == 'POST':
        hostname = request.form['hostname']
        new_node = Node(hostname)
        network.store_new_node(new_node)
    return render_template('peer.html', peers=peers)


@app.route("/key", methods=['GET'])
def user_key_info():
    key_pair = get_key_pair_from_memory()
    key = json.loads(key_pair)
    return render_template('key.html', key=key)


@app.route("/transactions", methods=['GET'])
def get_transactions():
    key_pair = get_key_pair_from_memory()
    key = json.loads(key_pair)
    blockchain_base = get_blockchain_from_memory()
    utxo = blockchain_base.get_user_utxos(key['public key hash'])
    sent = blockchain_base.get_user_sent(key['public key hex'])
    return render_template('transactions.html', utxo=utxo, sent=sent)


@app.route("/get_block", methods=['GET'])
def get_block():
    pow = ProofOfWork(network)
    pow.create_new_block()
    pow.broadcast()
    return True


@app.route('/', methods=['GET', 'POST'])
def index():
    key = json.loads(get_key_pair_from_memory())["public key hash"]
    utxos = get_blockchain_from_memory().get_user_utxos(key)
    if request.method == 'POST':
        address = request.form['address']
        amount = int(request.form['amount'])
        utxo = utxos['utxos'][0]
        balance = utxo['amount'] - amount
        owner = Owner(private_key=private_key)
        wallet = Wallet(owner, network)
        input_0 = TransactionInput(transaction_hash=utxo['transaction_hash'], output_index=utxo['output_index'])
        output_0 = TransactionOutput(public_key_hash=address, amount=amount)
        if balance > 0:
            output_1 = TransactionOutput(public_key_hash=key, amount=balance)
            wallet.process_transaction(inputs=[input_0], outputs=[output_0, output_1])
        elif balance <= 0:
            return render_template('index.html', key=key, utxos=utxos,
                                   error="An error occurred, there is not enough balance to complete this transaction.")
        else:
            wallet.process_transaction(inputs=[input_0], outputs=[output_0])
        return render_template('index.html', key=key, utxos=utxos,
                               message="The Payment request has been successfully created and waiting for it to be "
                                       "added to the blockchain.")
    else:
        return render_template('index.html', key=key, utxos=utxos)


def main():
    global network
    my_node = Node(request.host)
    network = Network(my_node)
    network.join_network()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)


if __name__ == "__main__":
    main()
