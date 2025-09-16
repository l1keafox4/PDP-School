import base64
from cryptography.fernet import Fernet

# password = str(input("Enter your password:"))
# print(password)
# enc = base64.b64encode(password.encode("utf-8"))
# print(enc)
# dec = base64.b64decode(enc.decode("utf-8"))
# print(dec)


message ="GULP QLOQ GLUP"

key = Fernet.generate_key()

fernet = Fernet(key)

encMessage = fernet.encrypt(message.encode())

print(message)
print(encMessage)