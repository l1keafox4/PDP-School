import base64
data = str(input(": "))

encoded = base64.b64encode(data.encode('utf-8'))
print("Encode:", encoded)

decoded = base64.b64decode(encoded).decode('utf-8')
print("Decode:", decoded)