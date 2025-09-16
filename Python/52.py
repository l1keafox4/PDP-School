# def tekshir_string(value):
#     if isinstance(value, str) and not value.isdigit():
#         return True
#     else:
#         return False

# input_value = input(": ")
# result = tekshir_string(input_value)
# print(result)

# class User:
#     def __init__(self, username, password):
#         self.username = username
#         self.password = password

# def register_user(username, password, user_list):
#     for user in user_list:
#         if user.username == username:
#             print("Bu non uje bor")
#             return

#     new_user = User(username, password)
#     user_list.append(new_user)
#     print(f"{new_user.username} togri")

# def login_user(username, password, user_list):
#     for user in user_list:
#         if user.username == username and user.password == password:
#             print(f"{username} togri")
#             return

#     print("Foydalanuvchi nomi yoki paroli noto'g'ri.")

# registered_users = []

# register_user("Jasur", "secure_password", registered_users)
# login_user("Jasur", "secure_password", registered_users)
# login_user("Jasurbek", "password123", registered_users)

# def test_list(lst):
#     return isinstance(lst, list)

# input_list = [1, 2, 3, 4, 5]
# list_result = test_list(input_list)
# print(list_result)

