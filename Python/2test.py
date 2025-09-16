import yaml
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import exceptions
from l import TOKEN
import os

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    user_info = {
        'username': message.from_user.username,
        'fullname': message.from_user.full_name,
        'id': message.from_user.id
    }

    if os.path.exists('users.yaml'):
        with open('users.yaml', 'r') as file:
            users = yaml.safe_load(file) or []
    else:
        users = []

    if isinstance(users, list):
        id = [user.get('id') for user in users if isinstance(user, dict)]
        if user_info['id'] not in id:
            with open('users.yaml', 'a') as file:
                yaml.dump(user_info, file)

    await message.reply("Assalomu aleykum!")

if __name__ == '__main__':
    asyncio.run(dp.start_polling())