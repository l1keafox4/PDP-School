import sqlite3

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Register:
    def __init__(self):
        self.db_name = 'users.db'
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)
            conn.commit()

    def add_user(self, username, password):
        # Add a new user to the database
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                print(f"User '{username}' successfully registered.")
            except sqlite3.IntegrityError:
                print(f"Username '{username}' is already taken. Please choose a different username.")

class Login:
    def __init__(self):
        self.db_name = 'users.db'
        self.current_user = None

    def authenticate(self, username, password):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()    
            if user:
                self.current_user = User(username, password)
                print(f"Successful login. Your username is '{username}'.")
                return True
            else:
                print("Incorrect username or password. Login failed.")
                return False

def main():
    print("Welcome to the User Authentication System!")
    registration_system = Register()
    login_system = Login()

    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == '1':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            registration_system.add_user(username, password)
        elif choice == '2':
            while True:
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                if login_system.authenticate(username, password):
                    break
        elif choice == '3':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
