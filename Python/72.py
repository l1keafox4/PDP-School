import threading
import time

# def kichik_harflar(matn):
#     harflar = [harf for harf in matn if harf.islower()]
#     print(*harflar)

# matn = "Qale nima gap! Hello world!"
# thread = threading.Thread(target=kichik_harflar, args=(matn))
# thread.start()

def print_numbers():
    for x in range(5):
        time.sleep(1)
        print(f"Print Numbers: {x}")

def print_letters():
    for i in "LOX":
        time.sleep(1)
        print(f"Print Letters: {i}")

thread_letters = threading.Thread(target=print_letters)
thread_numbers = threading.Thread(target=print_numbers)

thread_letters.start()
thread_numbers.start()
thread_letters.join()
thread_numbers.join()
