import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.dispatcher.filters import Command
logging.basicConfig(level=logging.INFO)
mytoken = '6652182496:AAGx3FTlkqe0YZrUVtaTmdCt2g0JMdmortg'

bot = Bot(token=mytoken)

dp = Dispatcher(bot)


@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f" {message.from_user.first_name} Salom ")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
