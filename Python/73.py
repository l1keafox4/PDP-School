import requests
import json
import threading

def posts():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    data = response.json()
    with open("posts2.json", "w") as f:
        json.dump(data, f, indent=4)

def albums():
    url = "https://jsonplaceholder.typicode.com/albums"
    response = requests.get(url)
    data = response.json()
    with open("albums1.json", "w") as f:
        json.dump(data, f, indent=4)


def file(file_name):
    with open(file_name, "r") as f:
        data = json.load(f)
        print(data)

post_thread = threading.Thread(target=posts)
album_thread = threading.Thread(target=albums)

post_thread.start()
album_thread.start()

post_thread.join()
album_thread.join()

file("posts2.json")
file("albums1.json")