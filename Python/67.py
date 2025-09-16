import requests
import json

posts_response = requests.get("https://jsonplaceholder.typicode.com/posts")
posts_data = posts_response.json()

with open("posts.json", "w") as posts_file:
    json.dump(posts_data, posts_file, indent=3)

users_response = requests.get("https://jsonplaceholder.typicode.com/users")
users_data = users_response.json()

with open("users.json", "w") as users_file:
    json.dump(users_data, users_file, indent=3)
