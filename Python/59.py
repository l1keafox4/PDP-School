import requests

url = "https://jsonplaceholder.typicode.com/users"
jasur = requests.get(url)

if jasur.status_code == 200:
    with open("users.txt", "w") as file:
        file.write(jasur.text)
    print("Done")
else:
    print(jasur.status_code)