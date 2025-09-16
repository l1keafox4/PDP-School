import hashlib
import time

# lox = "Ethir 5" + str(time.time())

# hash0 = hashlib.md5(str(lox).encode("utf-8")).hexdigest()
# hash1 = hashlib.sha256(str(lox).encode("utf-8")).hexdigest()
# hash2 = hashlib.sha384(str(lox).encode("utf-8")).hexdigest()
# hash3 = hashlib.blake2b(str(lox).encode("utf-8")).hexdigest()
# hash4 = hashlib.sha512(str(lox).encode("utf-8")).hexdigest()

# print(f"{hash0}\n{hash1}\n{hash2}\n{hash3}\n{hash4}")+

def hashing(data: str):
    sha256 = hashlib.sha256(data.encode("utf-8"))
    return sha256.hexdigest()

fox = hashing(str(input(": ")))
print(fox)