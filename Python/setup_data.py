# setup_data.py

def setup_data():
    users = {
        'user1': {'username': 'john_doe', 'email': 'john@example.com', 'age': 25},
        'user2': {'username': 'jane_doe', 'email': 'jane@example.com', 'age': 30},
        'user3': {'username': 'bob_smith', 'email': 'bob@example.com', 'age': 22}
    }
    return users

if __name__ == "__main__":
    test_users = setup_data()
    print(test_users)