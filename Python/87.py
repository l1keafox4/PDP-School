import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
import json

TOKEN = "6375882485:AAFt_DyB6DfKjheo3izaQJDqhVVIttMhRKU"
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет! {message.from_user.full_name}")
    await message.answer(" Нажмите Войти или Регистрация", reply_markup=keyboard)



    @dp.message()
    async def reg(message: Message, state: FSMContext):
        if message.text == "Регистрация":
            await state.set_state(Form.name)
            await message.answer("Ведите Имя")


@dp.message(Form.name)
async def usernames(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.username)
    await message.answer("Ведите почту")


@dp.message(Form.username)
async def passwords(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(Form.password)
    await message.answer("Ведите пароль")


@dp.message(Form.password)
async def finish(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await state.set_state(Form.finish)
    data = await state.get_data()
    await state.clear()
    await message.answer(
        "Успешная регистрация",
    )
    name = data.get("name", "Unknown")
    username = data.get("username", "Unknown")
    password = data.get("password", "Unknown")

    matn = f" Имя:{name}\nФамилия: {username}\n Пароль: {password}"
    await message.answer(text=matn)

    with open('user_data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)



    @dp.message()
    async def reg(message: Message, state: FSMContext):
        if message.text == "Войти":
            await state.set_state(Form.name)
            await message.answer("Ведите Почту")


@dp.message(Form.username)
async def passwords(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(Form.password)
    await message.answer("Ведите пароль")



@dp.message(Form.password)
async def finish(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await state.set_state(Form.finish)
    data = await state.get_data()
    await state.clear()
    await message.answer(
        "Успешная регистрация",
    )
    name = data.get("name", "Unknown")
    username = data.get("username", "Unknown")
    password = data.get("password", "Unknown")

    matn = f" Имя:{name}\nФамилия: {username}\n Пароль: {password}"
    await message.answer(text=matn)

    with open('user_data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if name == "main":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())