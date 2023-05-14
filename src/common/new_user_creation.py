import binascii
import os.path

from src.common.owner import Owner
import json

FILENAME = "src/doc/key_pair.json"
PRIVATE_KEY = "src/doc/private_key.py"


def generate_key_pair():
    owner = Owner()
    with open(PRIVATE_KEY, "w") as file_obj:
        file_obj.write(f"private_key = {owner.private_key.export_key(format='DER')}")
    dictionary = {
        "public key hash": owner.public_key_hash,
        "public key hex": owner.public_key_hex
    }
    with open(FILENAME, "w") as jsonFile:
        json.dump(dictionary, jsonFile)
    return json.dumps(dictionary, indent=2)


def get_key_pair_from_memory():
    if os.path.isfile(FILENAME):
        with open(FILENAME, "r") as file_obj:
            key_pair = file_obj.read()
        if not key_pair:
            key_pair = generate_key_pair()
    else:
        key_pair = generate_key_pair()
    return key_pair
