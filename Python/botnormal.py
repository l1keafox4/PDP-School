import random
import logging
import sqlite3
from datetime import date, datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor 
from c import TOKEN
from uz import texts
from rus import answers
from keyboards import korzinka
with sqlite3.connect("Tgbotnormal.db") as con:
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
admin_password = "usmonlox"

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    logging.info("Start command triggered.")
    user_id = message.from_user.id
    korzinka={}
    print(korzinka)
    if user_id not in User:
        User[user_id] = {'first_name': message.from_user.first_name, 'start_time': datetime.now(), 'language': 'russian'}

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [KeyboardButton("🇺🇿 O'zbekcha"), KeyboardButton("🇷🇺 Русский")]
    keyboard.add(*buttons)

    await bot.send_message(
        message.chat.id,
        "Выберите язык / Tilni tanlang:",
        reply_markup=keyboard
    )
@dp.message_handler(lambda message: message.text in ["🇺🇿 O'zbekcha", '🇷🇺 Русский'])
async def set_language(message: types.Message):
    logging.info("Language selected:", message.text)
    user_id = message.from_user.id
    language = 'russian'
    if message.text == "🇺🇿 O'zbekcha":
        language = 'uzbek'
        logging.info(f"User {user_id} selected Uzbek language.")
        await bot.send_message(message.chat.id, "Siz O'zbek tilini tanladingiz!")
    elif message.text == '🇷🇺 Русский':
        logging.info(f"User {user_id} selected Russian language.")
        await bot.send_message(message.chat.id, "Вы выбрали русский язык!")

    User[user_id]['language'] = language

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🛍 Продукты' if language == 'russian' else '🛍 Mahsulotlar')
    button2 = types.KeyboardButton('⚙️ Настройки' if language == 'russian' else '⚙️ Sozlamalar')
    button4 = types.KeyboardButton('🛒 Корзина' if language == 'russian' else '🛒 Savatcha')
    button3 = types.KeyboardButton('📄 Помощь' if language == 'russian' else '📄 Yordam')
    markup.row(button1)
    markup.row(button2, button3, button4)

    now = datetime.now().strftime("%H:%M:%S")
    greeting = ""

    if now < "12:00:00":
        greeting = texts[language]['welcome_morning'].format(name=message.from_user.first_name)
    elif now >= "12:00:00" and now < "18:00:00":
        greeting = texts[language]['welcome_afternoon'].format(name=message.from_user.first_name)
    else:
        greeting = texts[language]['welcome_evening'].format(name=message.from_user.first_name)

    await bot.send_message(message.chat.id, greeting, reply_markup=markup)

@dp.message_handler()
async def info(message):
    global counter_dict,quantity_korzinka,admin_password,korzinka_total,korzinka_displayed
    global cpp,korzinka_info,chosen_product,a,cpq,korzinka,price,photo_url,name1
    user_id = message.from_user.id
    language = User[user_id]['language']
    if message.text == '🛍 Mahsulotlar' or message.text == "🛍 Продукты":
        await categories(message)
        counter_dict = 0
        cpp = 0
    elif message.text == '/adminpanel':
        await adminpanel(message)
        counter_dict = 0 
    elif message.text == '⚙️ Sozlamalar' or message.text == "⚙️ Настройки":
        await settingsChapter(message)
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
    elif message.text == "🌐 Tilni o'zgartirish" or message.text == "🌐 Изменить язык":
        korzinka={}
        await start(message)
    elif message.text == '✏️ Dasturchiga yozish' or message.text == '✏️ Написать разработчику':
        await bot.send_message(message.chat.id,f"{'https://t.me/Jas_623007'}")
        await bot.send_message(message.chat.id,f"{'https://t.me/Jorayev_Behruz'}")
    elif message.text == "📄 Ma'lumotnoma" or message.text == '📄 Информация':
        await reference(message)
    elif message.text == '↩️ Orqaga'or message.text == '↩️ Назад':
        await categories(message)
    elif message.text == '↩️️ Orqaga qaytish' or message.text == '↩️ Обратно':
        await categories(message)
    elif message.text == '↩️ Menyuga qaytish' or message.text == '↩️️ Вернуться в меню':
        await welcome(message)
    elif message.text == "👈 Orqaga" or message.text == '👈 Назад':
        await settingsChapter(message)
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
        counter_dict = 0
        if row:
            price, photo_url = row
            if photo_url:
                message_text = (f"{name1}: 1 шт/кг {price} сум \n Вкус: Топ за свои деньги \n Качество: Лучшее \n Гарантия: 1 год" if language == "russian" else f"{name1}: 1 dona/kilo {price} so`m \n Mazzasi: Qiccu \n Siffati: Zor \n Garantiya: 1 yil")
                await bot.send_photo(message.chat.id, photo_url, caption=message_text)
            else:
                message_text = (f"{name1}: 1 шт/кг {price} сум" if language == "russian" else f"{name1}: 1 dona/kilo {price} so`m")
                await bot.send_message(message.chat.id, message_text)
            await increase_decrease(message)
        else:
            await bot.send_message(message.chat.id, f"Товар '{name1}' не найден" if language == "russian" else f"Bu '{name1}' mahsulot topilmadi")

    elif message.text == "+":
        counter_dict += 1
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('+')
        button2 = types.KeyboardButton('-')
        button3 = types.KeyboardButton('↩️ Назад' if language == 'russian' else '↩️ Orqaga')
        button4 = types.KeyboardButton('💸 Купить' if language == 'russian' else "💸 Sotib olish")
        button6 = types.KeyboardButton("🛒 Добавить в Корзинку" if language == 'russian' else "🛒 Savatcha qoshish")
        markup.row(button1, button2)
        markup.row(button3, button4)
        markup.row(button6)
        await bot.send_message(message.chat.id, f"{counter_dict} шт/кг" if language == "russian" else f'{counter_dict} dona/kilo', reply_markup=markup)
    elif message.text == '-' and counter_dict > 1: 
        counter_dict -= 1
        await bot.send_message(message.chat.id, f"{counter_dict} шт/кг" if language == "russian" else f'{counter_dict} dona/kilo')
    elif message.text == '-' and counter_dict == 1:
        await bot.send_message(message.chat.id, f"Кол-во не может быть меньше 1 кг/шт" if language == "russian" else '1 kilo/dona dan kam bolishi mumkun emas')
    elif message.text == "💸 Naqd pul" or message.text == "💸 Наличные":
        await order(message)
    elif message.text == '💳 Pay Me':
        await bot.send_message(message.chat.id, f"Переводите на 8600987654321 эту карту" if language == "russian" else "Shu 8600987654321 karta nomeriga tashlang")
        await order(message)
    elif message.text == "🚚 Buyurtma berish" or message.text == "🚚 Заказать":
        await bot.send_message(message.chat.id, f"Спасибо что выбрали наш магазин!!!😊" if language == "russian" else "Buyurtmangiz uchun raxmat!!!😊")
        await categories(message)
    elif message.text == "💸 Sotib olish" or message.text == '💸 Купить':
        await bot.send_message(message.chat.id, f"Ваши выбранные продукты: {name1}, {counter_dict} шт/кг,\n С вас {counter_dict * price} сум" if language == "russian" else f"Siz tanlagan mahsulotlar: {name1}, {counter_dict} dona/kilo,\n Siz dan {counter_dict * price} so`m boladi")
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

    elif message.text == "🛒 Добавить в Корзинку" or message.text == "🛒 Savatcha qoshish":
        if name1 not in korzinka:
            quantity_korzinka = counter_dict
            print(korzinka)
            print(quantity_korzinka)
            korzinka[name1] = {'price': price, 'quantity': counter_dict}
            await bot.send_message(message.chat.id, f"Ваш продукт был добавлен в корзинку" if language == "russian" else f"Siz tanlagan mahsulot savatchaga qoshildi")
        else:
            await bot.send_message(message.chat.id, f"Ваш продукт уже имеется в корзинке" if language == "russian" else "Bu mahsulot allaqachon savatchada mavjud")

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

    elif message.text == "🛒 Корзина" or message.text == "🛒 Savatcha":
        if korzinka and not korzinka_displayed:
            print(korzinka)
            print(quantity_korzinka)
            await korzina(message)
            language = User[message.from_user.id]['language']
            korzinka_info = ""
            korzinka_total = 0
            for key, value in korzinka.items():
                product_price = value['price']
                quantity_korzinka = value['quantity']
                korzinka_price = quantity_korzinka * product_price
                korzinka_total += korzinka_price
                korzinka_info += (f"{key} {quantity_korzinka} шт/кг: {korzinka_price} сум\n" if language == "russian" else f"{key} {quantity_korzinka} dona/kilo: {korzinka_price} so`m\n")
            await bot.send_message(message.chat.id, f"В вашей корзинке имеется:\n{korzinka_info}\nОбщая стоимость: {korzinka_total} сум" if language == "russian" else f"Sizning savatizda:\n{korzinka_info}\nUmumiy narx: {korzinka_total} so`m")
            korzinka_displayed = True
        elif not korzinka:
            await bot.send_message(message.chat.id, f"В вашей корзинке ничего нет" if language == "russian" else "Sizning savatizda hech narsa yoq")
        else:
            await bot.send_message(message.chat.id, f"Ваша корзинка уже открыта:{korzinka_info}" if language == "russian" else "Savatcha allaqachon ko`rsatildi")
        korzinka_displayed = False

    elif message.text == "💳 Sotib olish" or message.text == '💳 Купить':
        # await bot.send_message(message.chat.id, f"Siz tanlagan mahsulotlar: {chosen_product}, {cpq} dona/kilo;" if chosen_product == "" else f"\n {name1}, {counter_dict} dona/kilo,\n Siz dan {counter_dict * price + cpp * cpq} so`m boladi")
        await bot.send_message(message.chat.id, f"Ваши продукты: {korzinka_info} \n С вас {korzinka_total} сум" if language == "russian" else f"Siz tanlagan mahsulotlar: {korzinka_info} \n Siz dan {korzinka_total} so`m boladi")
        await pay_for(message)
    elif message.text == "❌ Mahsulot olib tashlash" or message.text== "❌ Убрать продукт":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for key,value in korzinka.items():
            keyboard.add(types.KeyboardButton(key))
        await bot.send_message(message.chat.id, f'Выберите продукт:' if language == 'russian' else f'Mahsulot tanlang:', reply_markup=keyboard)
    elif message.text in korzinka:
        print(korzinka)
        await remove(message)
    elif message.text == admin_password:
        await bot.send_message(message.chat.id, "Успешный вход в админ-панель" if language == "russian" else "Siz Admin-panel ga muvofaqiyatli kirdingiz")
    elif not message.text:
        language = User[message.from_user.id]['language']
        await bot.send_message(message.chat.id, texts[language]['products'])
    else:
        language = User[message.from_user.id]['language']
        response = random.choice(answers[language])
        await bot.send_message(message.chat.id, response)
async def welcome(message):
    user_id = message.from_user.id
    language = User[user_id]['language']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🛍 Продукты' if language == 'russian' else '🛍 Mahsulotlar')
    button2 = types.KeyboardButton('⚙️ Настройки' if language == 'russian' else '⚙️ Sozlamalar')
    button4 = types.KeyboardButton('🛒 Корзина' if language == 'russian' else '🛒 Savatcha')
    button3 = types.KeyboardButton('📄 Помощь' if language == 'russian' else '📄 Yordam')
    markup.row(button1)
    markup.row(button2, button3, button4)
    await bot.send_message(message.chat.id, 'Siz menyuga o\'tdingiz' if language == 'uzbek' else 'Вы вернулись в меню', reply_markup=markup)

async def categories(message):
    user_id = message.from_user.id
    language = User[user_id]['language']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🍏 Фрукты' if language == 'russian' else '🍏 Mevalar')
    button2 = types.KeyboardButton('🥕 Овощи' if language == 'russian' else '🥕 Sabzavotlar')
    button3 = types.KeyboardButton("🥛 Молочные продукты" if language == 'russian' else '🥛 Sut mahsulotlari')
    button4 = types.KeyboardButton("🥩 Мясо" if language == 'russian' else '🥩 Go`sht')
    button5 = types.KeyboardButton("🥗 Другие продукты" if language == 'russian' else '🥗 Boshqa mahsulotlar')
    button6 = types.KeyboardButton('↩️️ Вернуться в меню' if language == 'russian' else '↩️ Menyuga qaytish')
    markup.row(button1, button2)
    markup.row(button3, button4)
    markup.row(button5)
    markup.row(button6)
    await bot.send_message(message.chat.id, "Все продукты, которые сейчас продаются:" if language == 'russian' else "Hozir sotuvda bo\'lgan barcha mahsulotlar:", reply_markup=markup)

async def fruits(message):
    user_id = message.from_user.id
    language = User[user_id]['language']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(texts['russian']['Anor'] if language == 'russian' else texts['uzbek']['Anor'])
    button3 = types.KeyboardButton('🔹 Персик' if language == 'russian' else '🔹 Shaptoli')
    button2 = types.KeyboardButton('🔹 Яблоко' if language == 'russian' else '🔹 Olma')
    button4 = types.KeyboardButton('🔹 Груша' if language == 'russian' else '🔹 Nok')
    button5 = types.KeyboardButton('🗓 Категория' if language == 'russian' else '🗓 Kategoriya')
    markup.row(button5)
    markup.row(button1, button2)
    markup.row(button3, button4)
    await bot.send_message(message.chat.id, "Все продукты, которые сейчас продаются:" if language == 'russian' else "Hozir sotuvda bo\'lgan barcha mahsulotlar:", reply_markup=markup)
async def milk_products(message):
    user_id = message.from_user.id
    language = User[user_id]['language']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🔹 Мороженое' if language == 'russian' else '🔹 Muzqaymoq')
    button2 = types.KeyboardButton('🔹 Курт' if language == 'russian' else '🔹 Qurt')
    button3 = types.KeyboardButton('🔹 Сливки' if language == 'russian' else '🔹 Qaymoq')
    button4 = types.KeyboardButton('🔹 Молоко' if language == 'russian' else '🔹 Sut')
    button5 = types.KeyboardButton('🗓 Категория' if language == 'russian' else '🗓 Kategoriya')
    markup.row(button5)
    markup.row(button1, button2)
    markup.row(button3, button4)
    await bot.send_message(message.chat.id, "Все продукты, которые сейчас продаются:" if language == 'russian' else "Hozir sotuvda bo\'lgan barcha mahsulotlar:", reply_markup=markup)

async def korzina(message):
    user_id = message.from_user.id
    language = User[user_id]['language']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('❌ Убрать продукт' if language == 'russian' else '❌ Mahsulot olib tashlash')
    button2 = types.KeyboardButton('💳 Купить' if language == 'russian' else '💳 Sotib olish')
    button5 = types.KeyboardButton('↩️️ Вернуться в меню' if language =='russian' else '↩️ Menyuga qaytish')
    markup.row(button1, button2)
    markup.row(button5)
    await bot.send_message(message.chat.id, "Вы открыли корзину" if language == 'russian' else "Siz savatchani ochdiz", reply_markup=markup)
    # markup.row(button3, button4)

# async def adminpanel(message):
#     language = User[user_id]['language']
#     user_id = message.from_user.id
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     button5 = types.KeyboardButton('↩️ Menyuga qaytish')
#     markup.row(button5)

async def adminpanel(message):
    user_id = message.from_user.id
    language = User[user_id]['language']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button5 = types.KeyboardButton('↩️ Menyuga qaytish')
    markup.row(button5)
    await bot.send_message(message.chat.id, "Введите пароль" if language =="russian" else "Parolni terin", reply_markup=markup)
    # if message.text == admin_password:
    #     await bot.send_message(message.chat.id, "Успешный вход в админ-панель" if language == "russian" else "Siz Admin-panel ga muvofaqiyatli kirdingiz", reply_markup=markup)
    # else:
    #     await bot.send_message(message.chat.id, "Неверный пароль. Доступ запрещен." if language == "russian" else "Parolni notogri terdingiz.", reply_markup=markup)

async def remove(message):
    user_id = message.from_user.id
    language = User[user_id]['language']
    del korzinka[message.text]
    await bot.send_message(message.chat.id,"Этот продукт был убран из корзинки" if language == "russian" else "Mahsulot savatchadan olib tashlandi")
    await welcome(message)

async def vegetables(message):
    user_id = message.from_user.id
    language = User[user_id]['language']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🔹 Помидор' if language == 'russian' else '🔹 Pomidor')
    button2 = types.KeyboardButton('🔹 Морковь' if language == 'russian' else '🔹 Sabzi')
    button3 = types.KeyboardButton('🔹 Огурец' if language == 'russian' else '🔹 Bodring')
    button4 = types.KeyboardButton('🔹 Картофель' if language == 'russian' else '🔹 Kartoshka')
    button5 = types.KeyboardButton('🗓 Категория' if language == 'russian' else '🗓 Kategoriya')
    markup.row(button5)
    markup.row(button1, button2)
    markup.row(button3, button4)
    await bot.send_message(message.chat.id, "Все продукты, которые сейчас продаются:" if language == 'russian' else "Hozir sotuvda bo\'lgan barcha mahsulotlar:", reply_markup=markup)

async def meat(message):
    user_id = message.from_user.id
    language = User[user_id]['language']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🔹 Говядина' if language == 'russian' else '🔹 Mol go`shti')
    button2 = types.KeyboardButton('🔹 Куриное мясо' if language == 'russian' else '🔹 Tovuq go`shti')
    button3 = types.KeyboardButton('🔹 Баранина' if language == 'russian' else '🔹 Qo`y go`shti')
    button4 = types.KeyboardButton('🔹 Говяжий Фарш' if language == 'russian' else '🔹 Qiyma go`shti(mol)')
    button5 = types.KeyboardButton('🗓 Категория' if language == 'russian' else '🗓 Kategoriya')
    markup.row(button5)
    markup.row(button1, button2)
    markup.row(button3, button4)
    await bot.send_message(message.chat.id, "Все продукты, которые сейчас продаются:" if language == 'russian' else "Hozir sotuvda bo\'lgan barcha mahsulotlar:", reply_markup=markup)

async def other_products(message):
    user_id = message.from_user.id
    language = User[user_id]['language']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🔹 Cheers' if language == 'russian' else '🔹 Cheers')
    button2 = types.KeyboardButton('🔹 Snickers' if language == 'russian' else '🔹 Snickers')
    button3 = types.KeyboardButton('🔹 Мармелад' if language == 'russian' else '🔹 Marmelad')
    button4 = types.KeyboardButton('🔹 Печенье' if language == 'russian' else '🔹 Pechenye')
    button5 = types.KeyboardButton('🗓 Категория' if language == 'russian' else '🗓 Kategoriya')
    markup.row(button5)
    markup.row(button1, button2)
    markup.row(button3, button4)
    await bot.send_message(message.chat.id, "Все продукты, которые сейчас продаются:" if language == 'russian' else "Hozir sotuvda bo\'lgan barcha mahsulotlar:", reply_markup=markup)


async def settingsChapter(message):
    user_id = message.from_user.id
    language = User[user_id]['language']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🌐 Изменить язык' if language == 'russian' else "🌐 Tilni o'zgartirish")
    button3 = types.KeyboardButton('↩️️ Вернуться в меню' if language == 'russian' else '↩️ Menyuga qaytish')
    markup.row(button1, button3)
    await bot.send_message(message.chat.id, "Выберите Настройки.\nВыберите вариант:" if language == 'russian' else 'Sozlamalar bo\'limi.\nBir variantni tanlang:', reply_markup=markup)


async def infoChapter(message):
    user_id = message.from_user.id
    language = User[user_id]['language']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('✏️ Написать разработчику' if language == 'russian' else '✏️ Dasturchiga yozish')
    button2 = types.KeyboardButton('↩️️ Вернуться в меню' if language == 'russian' else '↩️ Menyuga qaytish')
    button3 = types.KeyboardButton('📄 Информация' if language == 'russian' else "📄 Ma'lumotnoma")
    markup.row(button1, button3)
    markup.row(button2)
    await bot.send_message(message.chat.id, "Писать в поддержку.\n Здесь вы можете написать сообщение разработчику." if language == 'russian' else 'Yordam bo\'limi.\nBu erda siz dasturchiga xabar yozishingiz mumkin.',
                           reply_markup=markup)


async def increase_decrease(message):
    user_id = message.from_user.id
    language = User[user_id]['language']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('+')
    button2 = types.KeyboardButton('-')
    markup.row(button1, button2)
    await bot.send_message(message.chat.id, 'Сколько килограмов вы хотите?' if language == 'russian' else 'Necha kilo olmoqchisiz?', reply_markup=markup)


async def pay_for(message):
    user_id = message.from_user.id
    language = User[user_id]['language']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("💸 Наличные" if language == 'russian' else '💸 Naqd pul')
    button2 = types.KeyboardButton('💳 Pay Me' if language == 'russian' else '💳 Pay Me')
    button3 = types.KeyboardButton("↩️ Обратно" if language == 'russian' else '↩️️ Orqaga qaytish')
    markup.row(button1, button2)
    markup.row(button3)
    await bot.send_message(message.chat.id, "Выберите метод оплаты💸:" if language == 'russian' else  "To'lov usulini tanlang💸:", reply_markup=markup)

# async def order(message):
#     user_id = message.from_user.id
#     language = User[user_id]['language']

#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     button1 = types.KeyboardButton('🚚 Заказать' if language == 'russian' else "🚚 Buyurtma berish")
#     button2 = types.KeyboardButton('↩️ Назад' if language == 'russian' else "↩️ Orqaga")
#     markup.row(button1)
#     markup.row(button2)
#     await bot.send_message(message.chat.id, "", reply_markup=markup)

async def order(message):
    user_id = message.from_user.id
    language = User[user_id]['language']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🚚 Заказать' if language == 'russian' else "🚚 Buyurtma berish")
    button2 = types.KeyboardButton('↩️ Назад' if language == 'russian' else "↩️ Orqaga")
    markup.row(button1)
    markup.row(button2)
    photo_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmWUTqAhTw20Z-XS0LRKM2CzjKetp93S9CYPoQdaHUdw&s'
    caption = 'Или просканируйте QR-Code' if language == 'russian' else 'Yoki QR-Codeni skanerlang'
    await bot.send_photo(message.chat.id, photo_url, caption=caption, reply_markup=markup)

async def order1(message):
    user_id = message.from_user.id
    language = User[user_id]['language']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🚚 Заказать' if language == 'russian' else "🚚 Buyurtma berish")
    button2 = types.KeyboardButton('↩️ Назад' if language == 'russian' else "↩️ Orqaga")
    markup.row(button1)
    markup.row(button2)
    await bot.send_message(message.chat.id, """860098765432109 Shu kartaga tashleng
                        Siz mahsulotlarni 1 soat ichida qaytarish imkoniyatiz bor""", reply_markup=markup)


async def reference(message):
    await bot.send_message(message.chat.id, f"""About:
    Date of release: 18.11.2023
    Version: 5.4
    Last update: 04.04.2024
    Developers: Behruz Jo'rayev
    Jasurbek Zokirov""")    

if __name__ == '__main__':
    logging.info("R u sure about that?")
    executor.start_polling(dp, skip_updates=True)
    