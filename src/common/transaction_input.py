import json


class TransactionInput:
    def __init__(self, transaction_hash: str, output_index: int, unlocking_script: str = ""):
        self.transaction_hash = transaction_hash
        self.output_index = output_index
        self.unlocking_script = unlocking_script

    def to_json(self, with_unlocking_script: bool = True) -> str:
        return json.dumps(self.to_dict(with_unlocking_script))

    def to_dict(self, with_unlocking_script: bool = True):
        if with_unlocking_script:
            return {
                "transaction_hash": self.transaction_hash,
                "output_index": self.output_index,
                "unlocking_script": self.unlocking_script
            }
        else:
            return {
                "transaction_hash": self.transaction_hash,
                "output_index": self.output_index
            }
