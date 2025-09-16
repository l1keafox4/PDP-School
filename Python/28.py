import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.dispatcher.filters import Command
import webbrowser
from aiogram.utils import executor
from c import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

answers = ['Я не понял, что ты хочешь сказать.', 'Извини, я тебя не понимаю.', 'Я не знаю такой команды.', 'Мой разработчик не говорил, что отвечать в такой ситуации... >_<']

# Обработка команды /start
@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    # Добавляем кнопки, которые будут появляться после ввода команды /start
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🛍 Товары')
    button2 = types.KeyboardButton('⚙️ Настройки')
    button3 = types.KeyboardButton('📄 Справка')
    # Разделяю кнопки по строкам так, чтобы товары были отдельно от остальных кнопок
    markup.row(button1)
    markup.row(button2, button3)

    if message.text == '/start':
        # Отправляю приветственный текст
        await message.answer(f'Привет, {message.from_user.first_name}!\nУ меня ты сможешь купить некоторые товары!\nКонтакт моего разработчика: https://t.me/Jorayev_Behruz', reply_markup=markup)
    else:
        await message.answer('Перекинул тебя в главном меню! Выбирай!', reply_markup=markup)

# Обработка фото. Если пользователь пришлет фото, то бот отреагирует на него. Можно реализовать свой функционал
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def get_photo(message: types.Message):
    await message.answer('У меня нет возможности просматривать фото :(')

# Обработка обычных текстовых команд, описанных в кнопках
@dp.message_handler()
async def info(message: types.Message):
    if message.text == '🛍 Товары':
        await goodsChapter(message)
    elif message.text == '⚙️ Настройки':
        await settingsChapter(message)
    elif message.text == '📄 Справка':
        await infoChapter(message)
    elif message.text == '🔹 Anor #1':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Купить')
        button2 = types.KeyboardButton('↩️ Назад')
        markup.row(button1, button2)
        await message.answer('Информация о первом товаре...', reply_markup=markup)
    elif message.text == '🔹 Товар #2':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Купить')
        button2 = types.KeyboardButton('↩️ Назад')
        markup.row(button1, button2)
        await message.answer('Информация о втором товаре...', reply_markup=markup)
    elif message.text == '🔹 Товар #3':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Купить')
        button2 = types.KeyboardButton('↩️ Назад')
        markup.row(button1, button2)
        await message.answer('Информация о третьем товаре...', reply_markup=markup)
    elif message.text == '🔹 Товар #4':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Купить')
        button2 = types.KeyboardButton('↩️ Назад')
        markup.row(button1, button2)
        await message.answer('Информация о четвертом товаре...', reply_markup=markup)
    elif message.text == '⚙️ Настройки #1':
        # Функционал не придумал
        await message.answer('Настройки номер 1...')
    elif message.text == '⚙️ Настройки #2':
        # Функционал не придумал
        await message.answer('Настройки номер 2...')
    elif message.text == '💳 Купить' or message.text == '✏️ Написать разработчику':
        # Сюда можете ввести свою ссылку на Телеграмм, тогда пользователя будет перекидывать к вам в личку
        await webbrowser.open('https://t.me/Jorayev_Behruz', )
    elif message.text == '↩️ Назад':
        await goodsChapter(message)
    elif message.text == '↩️ Назад в меню':
        await welcome(message)
    # Если пользователь написал свое сообщение, то бот рандомно генерирует один из возможных вариантов ответа

# Добавлять и редактировать варианты ответов можно в списке answers
    else:
        await message.answer(answers[random.randint(0, 3)])

# Функция, отвечающая за раздел товаров
async def goodsChapter(message: types.Message):
    # Кнопки для товаров
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🔹 Anor #1')
    button2 = types.KeyboardButton('🔹 Товар #2')
    button3 = types.KeyboardButton('🔹 Товар #3')
    button4 = types.KeyboardButton('🔹 Товар #4')
    button5 = types.KeyboardButton('↩️ Назад в меню')
    markup.row(button1, button2)
    markup.row(button3, button4)
    markup.row(button5)

    # Отправляем сообщение с прикрепленными к нему кнопками товаров
    await message.answer('Вот все товары, которые сейчас находятся в продаже:', reply_markup=markup)

# Функция, отвечающая за раздел настроек
async def settingsChapter(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('⚙️ Настройки #1')
    button2 = types.KeyboardButton('⚙️ Настройки #2')
    button3 = types.KeyboardButton('↩️ Назад в меню')
    markup.row(button1, button2)
    markup.row(button3)
    await message.answer('Раздел настроек.\nВыбери один из вариантов:', reply_markup=markup)

# Функция, отвечающая за раздел помощи
async def infoChapter(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('✏️ Написать разработчику')
    button2 = types.KeyboardButton('↩️ Назад в меню')
    markup.row(button1, button2)
    await message.answer('Раздел справки.\nЗдесь ты можешь написать моему разработчику.', reply_markup=markup)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)