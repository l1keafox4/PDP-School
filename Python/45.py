class Person:
    def __init__(self, first_name, username, age):
        self.first_name = first_name
        self.username = username
        self.age = age
    def get_info(self):
        return self.first_name, self.username, self.age

    class User:
        def __init__(self, first_name, username, age):
            self.first_name = first_name[:15]
            self.age = max(age, 24)
            self.username = username.strip('@')


    

    @property
    def username_(self):
        return f"o'zgartitilgan username: {self.username}"

    @username_.setter
    def username_(self, new_username):
        self.username = new_username


person = Person("Jasurbek", "admin", 23)
print("oldin: ", *person.get_info())
person.username_ = "Jas@623"
print("hozir: ", *person.get_info())