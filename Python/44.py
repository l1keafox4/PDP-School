class Age:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def check_age(self):
        if self.age < 18:
            print(f"Salom, {self.name}! Kirish mumkun emas!")
        else:
            print(f"Salom, {self.name}! Xush kelibsiz!")

if __name__ == "__main__":
    try:
        user_name = input("Ism: ")
        user_age = int(input("Yosh: "))
        user = Age(user_name, user_age)
        user.check_age()
    except ValueError:
        print("Xato: error 404")
