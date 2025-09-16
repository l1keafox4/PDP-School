import yaml

data = {
    'name': 'Pdpschool',
    'age': '',
    'location': 'Uzb',
    'fullname': {
        "first_name": 'Jasur',
        "last_name": 'Zokirov'
    },
    "birthday": {
        "day": '13',
        "month": '12',
        "year": '2008'
    }
}

with open("users.yaml", "w") as users_file:
    yaml.dump(data,users_file)