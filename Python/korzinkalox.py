from datetime import date, datetime
import random
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from c import TOKEN
import sqlite3
with sqlite3.connect("Tgbot1.db") as con:
    cur = con.cursor()


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

User = {}
counter_dict = 0
cpp = 0
chosen_products = {}
korzinka_info = ''
korzinka_total = ""
korzinka_price = ''
korzinka_displayed = False
name1 = ''

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    logging.info("Start command triggered.")
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Anor')
    button2 = types.KeyboardButton('Olma')
    markup.row(button1)
    markup.row(button2)
    await bot.send_message(message.chat.id, "Assalomu Aleykum! Men orqali siz ba'zi mahsulotlarni sotib olishingiz mumkin!", reply_markup=markup)
@dp.message_handler()
async def info(message):
    global counter_dict
    global cpp
    global cpq
    global korzinka_info
    global chosen_product
    global name1
    global price
    global korzinka
    global korzinka_displayed
    global korzinka_price
    global korzinka_total
    global quantity_korzinka
    user_id = message.from_user.id
    if message.text == "+":
        counter_dict += 1
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('+')
        button2 = types.KeyboardButton('-')
        button3 = types.KeyboardButton('↩️ Orqaga')
        button6 = types.KeyboardButton("🛒 Savatcha qoshish")
        markup.row(button1, button2)
        markup.row(button3)
        markup.row(button6)
        await bot.send_message(message.chat.id,f'{counter_dict} dona/kilo', reply_markup=markup)
    elif message.text == '-' and counter_dict > 1: 
        counter_dict -= 1
        await bot.send_message(message.chat.id,f'{counter_dict} dona/kilo')
    elif message.text == '-' and counter_dict == 1:
        await bot.send_message(message.chat.id,'1 kilo/dona dan kam bolishi mumkun emas')
    elif message.text == "🛒 Savatcha qoshish":
        if name1 not in korzinka:
            await bot.send_message(message.chat.id,f"Siz tanlagan mahsulot savatchaga qoshildi")
        else:
            await bot.send_message(message.chat.id,"Bu mahsulot allaqachon savatchada mavjud")
    elif message.text == "Olma":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('+')
        markup.row(button1)
        await bot.send_message(message.chat.id, f'Siz Anor tanladingiz', reply_markup=markup)

    elif message.text == "Anor":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('+')
        markup.row(button1)
        await bot.send_message(message.chat.id, f'Siz Anor tanladingiz', reply_markup=markup)
    elif message.text == '↩️ Orqaga' or message.text == '↩️ Назад':
        await (message)
    elif message.text == "🛒 Корзинка" or message.text == "🛒 Savatcha":
        if korzinka and not korzinka_displayed:
            await korzina(message)
            korzinka_info = ""
            korzinka_price = 0
            korzinka_total = 0
            for key, value in korzinka.items():
                korzinka_price = quantity_korzinka * value
                korzinka_total += korzinka_price
                korzinka_info += (f"{key} {quantity_korzinka} dona/kilo: {korzinka_price} so`m\n")
            await bot.send_message(message.chat.id,f"Sizning savatizda:\n{korzinka_info}")
            korzinka_displayed = True
        elif not korzinka:
            await bot.send_message(message.chat.id,"Sizning savatizda hech narsa yoq")
        else:
            await bot.send_message(message.chat.id,"Savatcha allaqachon ko`rsatildi")
        korzinka_displayed = False


async def welcome(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🛍 Mahsulotlar')
    button2 = types.KeyboardButton('⚙️ Sozlamalar')
    button4 = types.KeyboardButton('🛒 Savatcha')
    button3 = types.KeyboardButton('📄 Yordam')
    markup.row(button1)
    markup.row(button2, button3, button4)
    await bot.send_message(message.chat.id,'Вы вернулись в меню', reply_markup=markup)


async def korzina(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button5 = types.KeyboardButton('↩️ Menyuga qaytish')
    markup.row(button5)
    await bot.send_message(message.chat.id,"Siz savatchani ochdiz", reply_markup=markup)
    # markup.row(button3, button4)


async def anor(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🛒 Savatcha qoshish')
    markup.row(button1)
    await bot.send_message(message.chat.id,"Siz tanlagan mahsulot savathchaga qoshildi", reply_markup=markup)

    
if __name__ == '__main__':
    logging.info("Jelezo jaritsa")
    executor.start_polling(dp, skip_updates=True)