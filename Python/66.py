import json
from pprint import pprint

with open("user.json", "r") as file:
    data = json.load(file)
    pprint(data)
