import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message

TOKEN = "6779395505:AAH4UwhJONCSWrTmJQVtlqXdCEw5MRL-DRQ"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['random'])
async def random_number(message: types.Message):
    try:
        user_input = int(message.text.split(' ')[1])
    except IndexError:
        await message.reply("Boshqacha son kiriting.")
        return
    except ValueError:
        await message.reply("Iltimos son kiriting.")
        return

    random_num = random.randint(1, 100)
    if random_num == user_input:
        response = "Siz togri toptingiz"
    else:
        response = "Siz topaolmadiz"
        
    await message.reply(response)
    await message.reply(f'Bu {random_num} edi')


async def main():
    await dp.start_polling()


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
