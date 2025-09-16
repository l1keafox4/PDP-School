import json
jasur = 'Hello World!'
with open('data.json', "w") as file:
    json.dump(jasur, file)
