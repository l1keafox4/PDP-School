import random
import logging
import sqlite3
from datetime import date, datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor 
from l import TOKEN
from uz import texts
from rus import answers
from keyboards import korzinka
with sqlite3.connect("Tgbot1.db") as con:
    cur = con.cursor()


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)
korzinka={}
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
async def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🛍 Mahsulotlar')
    button2 = types.KeyboardButton('⚙️ Hamkorlik')
    button4 = types.KeyboardButton('🛒 Savatcha')
    button3 = types.KeyboardButton('📄 Yordam')
    markup.row(button1)
    markup.row(button2, button3, button4)

    if message.text == '/start':
        now = datetime.now().strftime("%H:%M:%S")
        if now < "12:00:00": 
            await bot.send_message(message.chat.id, f"""Xayrli tong, {message.from_user.first_name}!\nMen orqali siz ba'zi mahsulotlarni sotib olishingiz mumkin!""", reply_markup=markup)
        elif now >= "12:00:00" and now < "18:00:00":
            await bot.send_message(message.chat.id, f"""Xayrli kun, {message.from_user.first_name}!\nMen orqali siz ba'zi mahsulotlarni sotib olishingiz mumkin!""", reply_markup=markup)
        else:
            await bot.send_message(message.chat.id,f"""Xayrli kech, {message.from_user.first_name}!\nMen orqali siz ba'zi mahsulotlarni sotib olishingiz mumkin!""", reply_markup=markup)
    else:
        await bot.send_message(message.chat.id, "Asosiy menyuga o'tilyapti! Tanlang!", reply_markup=markup)

@dp.message_handler()
async def info(message):
    global counter_dict
    global cpp
    global cpq
    global a
    global korzinka_info
    global chosen_product
    global name1
    global photo_url
    global price
    global korzinka
    global korzinka_displayed
    global korzinka_price
    global korzinka_total
    global quantity_korzinka
    user_id = message.from_user.id
    if message.text == '🛍 Mahsulotlar' or message.text == "🛍 Продукты":
        await categories(message)
        counter_dict = 0
        cpp = 0
        counter_dict = 0
    elif message.text == '🗓 Kategoriya' or message.text == '🗓 Категория':
        await categories(message)
        counter_dict = 0
    elif message.text == '📄 Yordam' or message.text == '📄 Помощь':
        await infoChapter(message)
        counter_dict = 0
    elif message.text == "🍏 Mevalar" or message.text == '🍏 Фрукты':
        await fruits(message)
        counter_dict = 0 
    elif message.text == '🥕 Sabzavotlar' or message.text == '🥕 Овощи':
        await vegetables(message)
        counter_dict = 0  
    elif message.text == '🥛 Sut mahsulotlari' or message.text == '🥛 Молочные продукты':
        await milk_products(message)
        counter_dict = 0 
    elif message.text == "🥩 Мясо" or message.text == '🥩 Go`sht':
        await meat(message)
        counter_dict = 0
    elif message.text == "🥗 Другие продукты" or message.text == '🥗 Boshqa mahsulotlar':
        await other_products(message)
        counter_dict = 0
    elif message.text == '✏️ Dasturchiga yozish':
        await bot.send_message(message.chat.id,f"{'https://t.me/Jas_623007'}")
    elif message.text == '⚙️ Hamkorlik':
        await bot.send_message(message.chat.id,f"{'https://t.me/Jas_623007'}")
    elif message.text == "📄 Ma'lumotnoma":
        await reference(message)
    elif message.text == '↩️ Orqaga':
        await categories(message)
    elif message.text == '↩️️ Orqaga qaytish':
        await categories(message)
    elif message.text == '↩️ Menyuga qaytish':
        await welcome(message)
    # elif message.text.startswith('🔹'):
    #     name1 = message.text[1:].strip()
    #     photo_url = ""
    #     cur.execute("SELECT price , link_p FROM product_prices WHERE product_name = ?", (name1,photo_url))
    #     # cur.execute("SELECT link_p FROM product_prices WHERE product_name = ?", (photo_url,))
    #     price_row = cur.fetchone()
    #     if price_row:
    #         price = price_row[0]
    #         message_text = (f"{name1}: 1 шт/кг {price} сум" if language == "russian" else f"{name1}: 1 dona/kilo {price} so`m")
    #         await bot.send_message(message.chat.id, message_text)
    #         await increase_decrease(message)
    #     else:
    #         await bot.send_message(message.chat.id, f"Товар '{name1}' не найден" if language == "russian" else f"Bu '{name1}' mahsulot topilmadi")
    elif message.text.startswith('🔹'):
        name1 = message.text[1:].strip()
        cur.execute("SELECT price, link_p FROM product_prices WHERE product_name = ?", (name1,))
        row = cur.fetchone()
        keyboard = InlineKeyboardMarkup()
        if row:
            price, photo_url = row
            if photo_url:
                callback_button = InlineKeyboardButton("INFO", callback_data='show_text')
                keyboard.add(callback_button)
                message_text = (f"{name1}: 1 dona/kilo {price} so`m")
                await bot.send_photo(message.chat.id, photo_url, caption=message_text, reply_markup=keyboard)
            else:
                keyboard.add(InlineKeyboardButton(text="", callback_data='show_text'))
                message_text = (f"{name1}: 1 dona/kilo {price} so`m")
                await bot.send_message(message.chat.id, message_text, reply_markup=keyboard)
            await increase_decrease(message)
        else:
            await bot.send_message(message.chat.id, f"Bu '{name1}' mahsulot topilmadi")

    elif message.text == "+":
        counter_dict += 1
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('+')
        button2 = types.KeyboardButton('-')
        button3 = types.KeyboardButton('↩️ Orqaga')
        button4 = types.KeyboardButton("💸 Sotib olish")
        button6 = types.KeyboardButton("🛒 Savatcha qoshish")
        markup.row(button1, button2)
        markup.row(button3, button4)
        markup.row(button6)
        await bot.send_message(message.chat.id, f'{counter_dict} dona/kilo', reply_markup=markup)
    elif message.text == '-' and counter_dict > 1: 
        counter_dict -= 1
        await bot.send_message(message.chat.id, f'{counter_dict} dona/kilo')
    elif message.text == '-' and counter_dict == 1:
        await bot.send_message(message.chat.id, f'1 kilo/dona dan kam bolishi mumkun emas')
    elif message.text == "💸 Naqd pul" or message.text == "💸 Наличные":
        await order(message)
    elif message.text == '💳 Pay Me':
        await order(message)
        await bot.send_message(message.chat.id, "Shu 8600987654321 karta nomeriga tashlang")
    elif message.text == "🚚 Buyurtma berish":
        await bot.send_message(message.chat.id, "Buyurtmangiz uchun raxmat!!!😊")
        await categories(message)
    elif message.text == "💸 Sotib olish":
        await bot.send_message(message.chat.id, f"Siz tanlagan mahsulotlar: {name1}, {counter_dict} dona/kilo,\n Siz dan {counter_dict * price} so`m boladi")
        await pay_for(message)
    # elif message.text == "🛒 Добавить в Корзинку" or message.text == "🛒 Savatcha qoshish":
    #     if name1 not in korzinka:
    #         korzinka[name1] = price
    #         quantity_korzinka = counter_dict
    #         print(korzinka)
    #         print(quantity_korzinka)
    #         await bot.send_message(message.chat.id, f"Ваш продукт был добавлен в корзинку" if language == "russian" else f"Siz tanlagan mahsulot savatchaga qoshildi")
    #     else:
    #         await bot.send_message(message.chat.id, f"Ваш продукт уже имеется в корзинке" if language == "russian" else "Bu mahsulot allaqachon savatchada mavjud")

    elif message.text == "🛒 Savatcha qoshish":
        if name1 not in korzinka:
            quantity_korzinka = counter_dict
            print(korzinka)
            print(quantity_korzinka)
            korzinka[name1] = {'price': price, 'quantity': counter_dict}
            await bot.send_message(message.chat.id, f"Siz tanlagan mahsulot savatchaga qoshildi")
        else:
            await bot.send_message(message.chat.id, f"Bu mahsulot allaqachon savatchada mavjud")

    # elif message.text == "🛒 Корзинка" or message.text == "🛒 Savatcha":
    #     if korzinka and not korzinka_displayed:
    #         await korzina(message)
    #         language = User[message.from_user.id]['language']
    #         korzinka_info = ""
    #         korzinka_price = 0
    #         korzinka_total = 0
    #         for key, value in korzinka.items():
    #             korzinka_price = quantity_korzinka * value
    #             korzinka_total += korzinka_price
    #             korzinka_info += (f"{key} {quantity_korzinka} шт/кг: {korzinka_price} сум\n" if language == "russian" else f"{key} {quantity_korzinka} dona/kilo: {korzinka_price} so`m\n")
    #         await bot.send_message(message.chat.id, f"В вашей корзинке имеется:\n{korzinka_info}" if language == "russian" else f"Sizning savatizda:\n{korzinka_info}")
    #         korzinka_displayed = True
    #     elif not korzinka:
    #         await bot.send_message(message.chat.id, f"В вашей корзинке ничего нет:{korzinka_info}" if language == "russian" else "Sizning savatizda hech narsa yoq")
    #     else:
    #         await bot.send_message(message.chat.id, f"Ваша корзинка уже открыта:{korzinka_info}" if language == "russian" else "Savatcha allaqachon ko`rsatildi")
    #     korzinka_displayed = False

    elif message.text == "🛒 Savatcha":
        if korzinka and not korzinka_displayed:
            print(korzinka)
            print(quantity_korzinka)
            await korzina(message)
            korzinka_info = ""
            korzinka_total = 0
            for key, value in korzinka.items():
                product_price = value['price']
                quantity_korzinka = value['quantity']
                korzinka_price = quantity_korzinka * product_price
                korzinka_total += korzinka_price
                korzinka_info += (f"{key} {quantity_korzinka} dona/kilo: {korzinka_price} so`m\n")
            await bot.send_message(message.chat.id, f"Sizning savatizda:\n{korzinka_info}\nUmumiy narx: {korzinka_total} so`m")
            korzinka_displayed = True
        elif not korzinka:
            await bot.send_message(message.chat.id, "Sizning savatizda hech narsa yoq")
        else:
            await bot.send_message(message.chat.id, "Savatcha allaqachon ko`rsatildi")
        korzinka_displayed = False

    elif message.text == "💳 Sotib olish" or message.text == '💳 Купить':
        # await bot.send_message(message.chat.id, f"Siz tanlagan mahsulotlar: {chosen_product}, {cpq} dona/kilo;" if chosen_product == "" else f"\n {name1}, {counter_dict} dona/kilo,\n Siz dan {counter_dict * price + cpp * cpq} so`m boladi")
        await bot.send_message(message.chat.id, f"Siz tanlagan mahsulotlar: {korzinka_info} \n Siz dan {korzinka_total} so`m boladi")
        await pay_for(message)
    elif message.text == "❌ Mahsulot olib tashlash":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for key,value in korzinka.items():
            keyboard.add(types.KeyboardButton(key))
        await bot.send_message(message.chat.id, f'Mahsulot tanlang:', reply_markup=keyboard)
    elif message.text in korzinka:
        print(korzinka)
        await remove(message)
    elif not message.text:
        await bot.send_message(message.chat.id, texts['products'])
    else:
        response = random.choice(answers)
        await bot.send_message(message.chat.id, response)

# @dp.callback_query_handler(lambda c: c.data == 'button_pressed')
# async def process_callback_button(callback_query: types.CallbackQuery):
#     await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == 'show_text')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id,text=f"""{name1}:{price} s`om
Mazasi: Qiccu
Siffati: 100%
Garantiya: """)


async def welcome(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🛍 Mahsulotlar')
    button2 = types.KeyboardButton('⚙️ Hamkorlik')
    button4 = types.KeyboardButton('🛒 Savatcha')
    button3 = types.KeyboardButton('📄 Yordam')
    markup.row(button1)
    markup.row(button2, button3, button4)
    await bot.send_message(message.chat.id, 'Siz menyuga o\'tdingiz', reply_markup=markup)

async def categories(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🍏 Mevalar')
    button2 = types.KeyboardButton('🥕 Sabzavotlar')
    button3 = types.KeyboardButton('🥛 Sut mahsulotlari')
    button4 = types.KeyboardButton('🥩 Go`sht')
    button5 = types.KeyboardButton('🥗 Boshqa mahsulotlar')
    button6 = types.KeyboardButton('↩️ Menyuga qaytish')
    markup.row(button1, button2)
    markup.row(button3, button4)
    markup.row(button5)
    markup.row(button6)
    await bot.send_message(message.chat.id, "Hozir sotuvda bo\'lgan barcha mahsulotlar:", reply_markup=markup)

async def fruits(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(texts['uzbek']['Anor'])
    button3 = types.KeyboardButton('🔹 Shaptoli')
    button2 = types.KeyboardButton('🔹 Olma')
    button4 = types.KeyboardButton('🔹 Nok')
    button5 = types.KeyboardButton('🗓 Kategoriya')
    markup.row(button5)
    markup.row(button1, button2)
    markup.row(button3, button4)
    await bot.send_message(message.chat.id, "Hozir sotuvda bo\'lgan barcha mahsulotlar:", reply_markup=markup)
async def milk_products(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🔹 Muzqaymoq')
    button2 = types.KeyboardButton('🔹 Qurt')
    button3 = types.KeyboardButton('🔹 Qaymoq')
    button4 = types.KeyboardButton('🔹 Sut')
    button5 = types.KeyboardButton('🗓 Kategoriya')
    markup.row(button5)
    markup.row(button1, button2)
    markup.row(button3, button4)
    await bot.send_message(message.chat.id, "Hozir sotuvda bo\'lgan barcha mahsulotlar:", reply_markup=markup)

async def korzina(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('❌ Mahsulot olib tashlash')
    button2 = types.KeyboardButton('💳 Sotib olish')
    button5 = types.KeyboardButton('↩️ Menyuga qaytish')
    markup.row(button1, button2)
    markup.row(button5)
    await bot.send_message(message.chat.id, "Siz savatchani ochdiz", reply_markup=markup)
    # markup.row(button3, button4)

async def remove(message):
    user_id = message.from_user.id
    del korzinka[message.text]
    await bot.send_message(message.chat.id, "Mahsulot savatchadan olib tashlandi")
    await welcome(message)

async def vegetables(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🔹 Pomidor')
    button2 = types.KeyboardButton('🔹 Sabzi')
    button3 = types.KeyboardButton('🔹 Bodring')
    button4 = types.KeyboardButton('🔹 Kartoshka')
    button5 = types.KeyboardButton('🗓 Kategoriya')
    markup.row(button5)
    markup.row(button1, button2)
    markup.row(button3, button4)
    await bot.send_message(message.chat.id, "Hozir sotuvda bo\'lgan barcha mahsulotlar:", reply_markup=markup)

async def meat(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🔹 Mol go`shti')
    button2 = types.KeyboardButton('🔹 Tovuq go`shti')
    button3 = types.KeyboardButton('🔹 Qo`y go`shti')
    button4 = types.KeyboardButton('🔹 Qiyma go`shti(mol)')
    button5 = types.KeyboardButton('🗓 Kategoriya')
    markup.row(button5)
    markup.row(button1, button2)
    markup.row(button3, button4)
    await bot.send_message(message.chat.id, "Hozir sotuvda bo\'lgan barcha mahsulotlar:", reply_markup=markup)

async def other_products(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🔹 Cheers')
    button2 = types.KeyboardButton('🔹 Snickers')
    button3 = types.KeyboardButton('🔹 Marmelad')
    button4 = types.KeyboardButton('🔹 Pechenye')
    button5 = types.KeyboardButton('🗓 Kategoriya')
    markup.row(button5)
    markup.row(button1, button2)
    markup.row(button3, button4)
    await bot.send_message(message.chat.id, "Hozir sotuvda bo\'lgan barcha mahsulotlar:", reply_markup=markup)

async def infoChapter(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('✏️ Dasturchiga yozish')
    button2 = types.KeyboardButton('↩️ Menyuga qaytish')
    button3 = types.KeyboardButton("📄 Ma'lumotnoma")
    markup.row(button1, button3)
    markup.row(button2)
    await bot.send_message(message.chat.id, 'Yordam bo\'limi.\nBu erda siz dasturchiga xabar yozishingiz mumkin.',
                           reply_markup=markup)


async def increase_decrease(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('+')
    button2 = types.KeyboardButton('-')
    markup.row(button1, button2)
    await bot.send_message(message.chat.id, 'Necha kilo olmoqchisiz?', reply_markup=markup)


async def pay_for(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('💸 Naqd pul')
    button2 = types.KeyboardButton('💳 Pay me')
    button3 = types.KeyboardButton('↩️️ Orqaga qaytish')
    markup.row(button1, button2)
    markup.row(button3)
    await bot.send_message(message.chat.id, "To'lov usulini tanlang💸:", reply_markup=markup)

async def order(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("🚚 Buyurtma berish")
    button2 = types.KeyboardButton("↩️ Orqaga")
    markup.row(button1)
    markup.row(button2)
    await bot.send_message(message.chat.id, "Siz mahsulotlarni 1 soat ichida qaytarish imkoniyatiz bor", reply_markup=markup)

async def order1(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("🚚 Buyurtma berish")
    button2 = types.KeyboardButton("↩️ Orqaga")
    markup.row(button1)
    markup.row(button2)
    await bot.send_message(message.chat.id, """860098765432109 Shu kartaga tashleng
                        Siz mahsulotlarni 1 soat ichida qaytarish imkoniyatiz bor""", reply_markup=markup)


async def reference(message):
    await bot.send_message(message.chat.id, f"""About:
    Date of release: 18.11.2023
    Version: 5.4
    Last update: 15.03.2024
    Developers: Behruz Jo'rayev
    Jasurbek Zokirov""")    

if __name__ == '__main__':
    logging.info("R u sure about that?")
    executor.start_polling(dp, skip_updates=True)
    