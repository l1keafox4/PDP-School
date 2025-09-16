
import random

min_num = 1
max_num = 100

secret_num = random.randint(min_num, max_num)

attempts = 10

print(f"Привет! Давай поиграем в игру. Я загадал число от {min_num} до {max_num}. Ты должен угадать его за {attempts} попыток. Поехали!")

for i in range(attempts):

  print(f"Попытка {i+1} из {attempts}.")

  guess = int(input("Введи свое число: "))

  if guess == secret_num:

    print("Поздравляю! Ты угадал число!")
    break 
  elif guess < secret_num:
    print("Твое число слишком маленькое. Попробуй еще раз.")
  else:
   
    print("Твое число слишком большое. Попробуй еще раз.")
else:

  print(f"К сожалению, ты не угадал число. Я загадал число {secret_num}. В следующий раз повезет больше!")