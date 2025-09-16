import requests
from pprint import pprint
# response_comments = requests.get('https://jsonplaceholder.typicode.com/comments?postId=1')
# comments = response_comments.json()
# print(": ")
# for comment in comments:
#     print(comment)  
# print()

response_users = requests.get('https://jsonplaceholder.typicode.com/users')
users = response_users.json()
print("2. Userlar ro'yxati:")
for user in users:
    pprint(user)
print()

# print("(email, address, phone):")
# for user in users:
#     user_info = {
#         'email': user['email'],
#         'address': user['address'],
#         'phone': user['phone']
#     }
#     print(user_info)