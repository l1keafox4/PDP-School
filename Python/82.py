import hashlib

def hash_func(password):
    hash_object = hashlib.sha256(password.encode())
    return hash_object.hexdigest()

def create_user():
    name = input("Ism: ")
    username = input("Username: ")
    password = input("Parol: ")
    hashed_password = hash_func(password)
    with open('hash.txt', 'w') as file:
        file.write(f"{username}: {hashed_password}\n")

if __name__ == "__main__":
    create_user()
