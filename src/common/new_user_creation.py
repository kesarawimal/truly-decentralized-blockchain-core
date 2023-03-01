import base64
import os.path

from common.owner import Owner
import json

FILENAME = "src/doc/key_pair.json"


def generate_key_pair():
    owner = Owner()
    dictionary = {
        "public key hash": owner.public_key_hash,
        "public key hex": owner.public_key_hex
        "private key": base64.b64encode(owner.private_key.export_key(format='DER')).decode('utf-8'),
    }
    with open(FILENAME, "w") as jsonFile:
        json.dump(dictionary, jsonFile)
    return json.dumps(dictionary, indent=3)


def get_key_pair_from_memory():
    if os.path.isfile(FILENAME):
        with open(FILENAME, "r") as file_obj:
            key_pair = file_obj.read()
        if not key_pair:
            key_pair = generate_key_pair()
    else:
        key_pair = generate_key_pair()
    return key_pair
