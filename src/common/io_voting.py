import json


FILENAME = "src/doc/voting"


def get_voting_from_memory() -> list:
    with open(FILENAME, "rb") as file_obj:
        try:
            current_voting_str = file_obj.read()
            current_voting_list = json.loads(current_voting_str)
        except:
            return []
    if current_voting_list is None:
        return []
    return current_voting_list


def store_voting_in_memory(voting: list):
    vote = get_voting_from_memory()
    vote.append(voting)
    text = json.dumps(vote).encode("utf-8")
    with open(FILENAME, "wb") as file_obj:
        file_obj.write(text)
