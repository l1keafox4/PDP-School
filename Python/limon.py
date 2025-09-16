from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from aiogram import executor
from geopy.geocoders import Nominatim
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher import FSMContext
import sqlite3
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
conn = sqlite3.connect('Tgbot1.db')
cursor = conn.cursor()
from keyboards import keyboards,find,info_ok,usernam,delivery_info,delivery,order_ok,keyboard_manager,find_manager,user,amount_edit,summa_edit,lang,current_value,button_exe
import random
from l import TOKEN
from geopy.distance import geodesic
import json
from datetime import datetime
from aiogram.types import LabeledPrice
import time

print("Online apteka bot v1.0")
PAYMENTS_TOKEN = '398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
address = ''
MANAGER_USER_ID = -4146568935

user_coordinates = {}
wait = 0
dp = Dispatcher(bot, storage=MemoryStorage())
cart = {}

# @dp.message_handler(commands=['id'])
# async def process_start_command(message: types.Message):
#     await message.answer(f"ID group {message.chat.id}")




# @dp.message_handler(commands=['adminpanel0258'])
# async def process_start_command(message: types.Message):
#     await message.answer(f"Админ панель включен 🟢")
#     await message.answer(f"Напишите название лекарства для изменения (Мин: 3 букв)")
#     global find_manager
#     find_manager = 1
# @dp.message_handler(commands=['adminpanel0258off'])
# async def process_start_command(message: types.Message):
#     await message.answer(f"Админ панель отключен 🔴")
#     global find_manager
#     find_manager = 0


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if lang == '':
        keyboard_lang = types.InlineKeyboardMarkup(resize_keyboard=True)
        keyboard_lang.add(InlineKeyboardButton("🇺🇿 O'zbek tili", callback_data='lang_uz'))
        keyboard_lang.add(InlineKeyboardButton("🇷🇺 Русский язык", callback_data='lang_ru'))
        await message.answer('Tilni tanlang | Выберите язык',reply_markup=keyboard_lang)
    else:

        global id_user
        global chat_id
        chat_id = message.chat.id
        cursor.execute('SELECT * FROM users WHERE id = ?',(message.chat.id,))
        id_user = cursor.fetchall()
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

        user = message.from_user
        username = user.first_name
        await message.answer(f"{('Привет', lang)}, <b>{username}</b>!", parse_mode=ParseMode.HTML)
        await message.answer(("Это онлайн бот Sevinch pharm", lang))
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton(("🔍 Поиск лекарств", lang)))
        print(id_user)
        if id_user != []:
            keyboard.add(KeyboardButton("👤 Профиль",lang))
            global info_ok
            global order_ok
            info_ok = 1
            order_ok = 1
            global orders
            global address
            global phone_number
            global delivery_info
            global delivery
            global usernam
            usernam = message.from_user.username
            cursor.execute("SELECT * FROM users WHERE id = ?", (message.chat.id,))
            info = cursor.fetchall()
            info = (info[0])
            phone_number = info[2]
            address = (info[1]).split("'")[1]
            orders = info[3]
            delivery = (info[1]).split(',')[0][1:]
            delivery_info = f"🚚 {('Доставка', lang)}: {info[1].split(',')[0][1:]} сум {lang} {info[1].split(',')[1][1:]}km ≈ {int(info[1].split(',')[2])+10} минут"
        else:

            keyboard.add(KeyboardButton(("📞 Дать телефон и местоположение"),lang))
        await message.answer(f"{('ℹ️ Выберите действие:', lang)}", reply_markup=keyboard)

@dp.callback_query_handler(text_contains = 'lang_')
async def setLanguage(callback: types.CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    global lang
    if callback.data[5:] == 'ru':
        lang = 'ru'
        await bot.send_message(callback.from_user.id, 'Успешно выбран язык\nНапишите: /start')
    if callback.data[5:] == 'uz':
        lang = 'uz'
        await bot.send_message(callback.from_user.id, 'Til tanlandi\nYozing: /start')      


@dp.message_handler(lambda message: message.text in(('📞 Дать телефон и местоположение', lang),('📞 Отправить заново телефон и местоположение', lang)))
async def get_chat_id(message: types.Message):
     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
     keyboard.add(KeyboardButton(("📍 Отправить местоположение", lang),request_location=True))
     await message.answer(("Сначала отправте мне вашу геопозицию", lang))
     await message.answer(("ℹ️ Выберите действие:", lang), reply_markup=keyboard)

@dp.message_handler(content_types=types.ContentType.LOCATION)
async def handle_location(message: types.Message):
     global latitude
     global longitude
     latitude = message.location.latitude
     longitude = message.location.longitude
 
     def get_address_from_coordinates(latitude, longitude):
         geolocator = Nominatim(user_agent="your_app_name")
         location = geolocator.reverse((latitude, longitude), language="ru")
         return location.address
     global address
     address = get_address_from_coordinates(latitude, longitude)
     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
     keyboard.add(KeyboardButton(("📞 Отправить номер телефона", lang), request_contact=True))
     await message.answer(("Ваша геопозиция успешно получена.\nТеперь мне нужно взять ваш номер телефона", lang),reply_markup=keyboard)
@dp.message_handler(content_types=types.ContentType.CONTACT)
async def handle_location(message: types.Message):
    user_id = message.from_user.id
    phone_number = message.contact.phone_number
    markup=types.ReplyKeyboardRemove()
    await message.answer("Ваш номер телефона успешно отправлен.\nОжидайте бот определяет ваши данные (Задержка ≈30-40секунд)")
    graph_area = ("Ташкент, Узбекистан")
    global usernam
    usernam = message.from_user.username
    global delivery_info,delivery
    # # Координаты двух точек
    # # Вычисление расстояния между точками 
    print(distance_in_meters)
    distance_in_meters = int(distance_in_meters)
    delivery = int(distance_in_meters/500)
    kilo = round(distance_in_meters/1000, 2)
    delivery = delivery*5000
    print(distance_in_meters)
    addresss = [] 
    addresss.append(delivery)
    addresss.append(kilo)
    addresss.append(int())
    addresss.append(address)
    cord = []
    cord.append(latitude)
    cord.append(longitude)
    cord_txt = json.dumps(cord)
    cursor.execute('SELECT * FROM users WHERE id = ?',(message.chat.id,))
    id_user = cursor.fetchall()
    if id_user == []:
        cursor.execute('INSERT INTO users VALUES (?,?,?,?,?,?)',(message.chat.id,str(addresss),phone_number,'', cord_txt,lang))
        conn.commit()
    else:
       id_user = list(id_user[0])
       cursor.execute(f'UPDATE users SET adress = ?, telephone = ?, cord = ? WHERE id = {message.chat.id}',(addresss,phone_number,cord_txt))
       conn.commit()
    global info_ok
    info_ok = 1
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(f'📞 Отправить заново телефон и местоположение'))
    keyboard.add(KeyboardButton(f'🛒 Корзина'))
    keyboard.add(KeyboardButton(f'🔍 Поиск лекарств'))
    await message.answer("Чтобы продолжить нажмите на кнопку ниже",reply_markup=keyboard)
@dp.message_handler(lambda message: message.text == '👤 Profil')
async def get_chat_id(message: types.Message):
    global orders
    global address
    global phone_number

    cursor.execute("SELECT * FROM users WHERE id = ?", (message.chat.id,))
    info = cursor.fetchall()
    info = (info[0])
    phone_number = info[2]
    address = (info[1]).split("'")[1]
    orders = info[3]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("🛍 Мои заказы"))
    keyboard.add(KeyboardButton("⬅️ Назад"))
    await message.answer(f"""
ℹ️ Вот ваши данные:
🆔 Username: @{message.from_user.username}
📞 Телефон номер: {phone_number}
📍 Адрес: {(info[1]).split("'")[1]}\n
🚚 Доставка в этот адрес обойдётся в {(info[1]).split(',')[0][1:]} {("сум", lang)} ({(info[1]).split(',')[1][1:]}km ≈ {int((info[1]).split(',')[2])+10} минут)

⚠️ Если вы удалите этот чат вашт данные могут быть стёрты ⚠️
""",reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == '🛍 Mening buyurtmalarim')
async def get_chat_id(message: types.Message):
   if order_ok == 1: 
    if orders == '':
        await message.answer('У вас нет заказов')
    else:
        cursor.execute('SELECT orders FROM users WHERE id = ?', (chat_id,))
        order_info = cursor.fetchall()[0]
        json_data = order_info
        # Десериализуем строку JSON обратно в список
        list_data = list(json.loads(json_data[0]))
        for i in list_data:
            cursor.execute('SELECT * FROM "order" WHERE id_order = ?', (i,))
            try:
                info = list(cursor.fetchall()[0])
            except:
                continue
            json_data = info[4]
            json_data1 = info[5]
            # Десериализуем строку JSON обратно в список
            # Десериализуем строку JSON обратно в список
            recipient_info = list(json.loads(json_data))
            address_info = list(json.loads(json_data1))
    await message.answer(f"""Заказ:№{info[0]}
--------------------------------
💊 Лекарства:
{info[1]}
--------------------------------
💲Оплата: {info[2]}{("сум", lang)}
💵 Способ оплаты: Наличные
--------------------------------
📍 Адрес: {info[3]}
{address_info[0]}
Статус: {address_info[1]}
--------------------------------
 Данные клиента:
🆔 Username: @{recipient_info[0]}
📞 Телефон номер: <code>+{recipient_info[1]}</code>
--------------------------------
🗓 Дата {info[6]}
    """, parse_mode=ParseMode.HTML)

@dp.message_handler(lambda message: message.text in ('⬅️ Ortga','⬅️ Назад'))
async def get_chat_id(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(("🔍 Поиск лекарств", lang)))
    if id_user != []:
        keyboard.add(KeyboardButton(("👤 Профиль", lang)))
    else:
        keyboard.add(KeyboardButton(("📞 Дать телефон и местоположение"),lang))
    await message.answer("ℹ️ Выберите действие:", reply_markup=keyboard)
@dp.message_handler(lambda message: message.text in ('💵 Наличные'))
async def get_chat_id(message: types.Message):
   if info_ok == 1:
    keyboardsss = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton("Потвердить заказ", callback_data='accept')]
                ])
    global nom
    cursor.execute('SELECT id_order FROM "order"')
    try:
        number = list(cursor.fetchall()[0])
    except:
        number = cursor.fetchall()
    a = 0
    b = []
    while a == 0:
        nom = random.randint(1000,9999)
        for i in number:
            if nom != i:
                b.append('TRUE')
            else:
                b.append('FALSE')
        if b.count('FALSE') == 0:
            a = 1

    await message.answer(f"""Заказ:№{nom}
--------------------------------
💊 Лекарства:
{cart_info}
--------------------------------
💲 К оплате: {formatted_total} {("сум", lang)}
💵 Способ оплаты: Наличные
--------------------------------
📍 Адрес: {address}
--------------------------------
{delivery_info}
--------------------------------
ℹ️ Когда заказ приедет вам позвонит курьер ℹ️
""", reply_markup=keyboardsss)
    global sposob_oplati
    sposob_oplati = '💵 Способ оплаты: Наличные'
   else:
       await message.answer('Вы не дали боту вашу локацию и номер')
       keyboard_loc = types.ReplyKeyboardMarkup(resize_keyboard=True)
       keyboard_loc.add(KeyboardButton(("📞 Дать телефон и местоположение"),lang))
       await message.answer("ℹ️ Выберите действие:", reply_markup=keyboard_loc)
@dp.message_handler(lambda message: message.text == '💳 Click (Временно не работает')
async def get_chat_id(message: types.Message):
   if info_ok == 1:
    keyboardsss = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(("Потвердить заказ", lang), callback_data='accept')]
                ])
    global nom
    global formatted_total
    cursor.execute('SELECT id_order FROM "order"')
    try:
        number = list(cursor.fetchall()[0])
    except:
        number = cursor.fetchall()
    a = 0
    b = []
    while a == 0:
        nom = random.randint(1000,9999)
        for i in number:
            if nom != i:
                b.append('TRUE')
            else:
                b.append('FALSE')
        if b.count('FALSE') == 0:
            a = 1
    await message.answer((f"""{("Заказ",lang)}:№{nom}
--------------------------------
💊 {("Лекарства", lang)}:
{cart_info}
--------------------------------
💲 {("К оплате", lang)}: {formatted_total} {("сум", lang)}
💳 {("Способ оплаты",lang)}: Click
--------------------------------
📍 {("Адрес",lang)}: {address}
--------------------------------
{delivery_info}
--------------------------------
{("ℹ️ Когда заказ приедет вам позвонит курьер ℹ️",lang)}
""", lang), reply_markup=keyboardsss)
    global sposob_oplati
    sposob_oplati = '💳 Способ оплаты: Click'
    prices = [LabeledPrice(label='Product 1', amount=int(formatted_total.replace('.',''))*100)]
    await bot.send_invoice(message.chat.id, title='Онлайн оплата через Click', description= 'Оплатите и потвердите', provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065', currency='UZS', prices=prices, payload='Лекарства', photo_url='https://avatars.dzeninfra.ru/get-zen_doc/271828/pub_6597bdf5df834a4869446684_6597be07df834a4869446c9a/scale_1200')

   else:
       await message.answer(('Вы не дали боту вашу локацию и номер', lang))
       keyboard_loc = types.ReplyKeyboardMarkup(resize_keyboard=True)
       keyboard_loc.add(KeyboardButton(("📞 Дать телефон и местоположение"),lang))
       await message.answer(("ℹ️ Выберите действие:", lang), reply_markup=keyboard_loc)

@dp.message_handler(lambda message: message.text in (('🛒 Корзина', lang)))
async def get_chat_id(message: types.Message):
   try: 
    reply_markup=types.ReplyKeyboardRemove()
    cart_sum = {}
    global formatted_total
    global cart_info
    cart_info = ""
    keyboardss = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton("Купить", callback_data='buy')]])
    # total = 0
    print(cart)
    for key, value in cart.items():
        print(f"{key} = {value}")
        cursor.execute("SELECT narxi,soni FROM dorilar WHERE nomi = ?", (key,))
        summa = cursor.fetchall()
        summa = list(summa[0])
        suma = int((summa[0][:-3]).replace(" ", ""))*int(value)
        amount = (summa[1]).replace(",", "")
        cart_sum[key] = suma 
        total = sum(int(value+int(delivery)) for value in cart_sum.values())
        print(total)
        formatted_sum = "{:,}".format(cart_sum[key]).replace(",", ".")
        cart_info += f"💊{key}|{value} {('шт.', lang)}|💵{('Стоимость', lang)}:{formatted_sum} {('сум', lang)}\n"
    formatted_total = "{:,}".format(total).replace(",", ".")
    await message.answer(f"""{("Вот ваши лекарства", lang)}:
{cart_info}------------------------------------------------
{delivery_info}
{("Общая стоимость", lang)}: {formatted_total} {("сум", lang)}
""", reply_markup=keyboardss)
   except:
    await message.answer(("Корзина пуста", lang))

@dp.message_handler(lambda message: message.text in (('🔍 Поиск лекарств', lang)))
async def get_chat_id(message: types.Message):
    global find
    reply_markup=types.ReplyKeyboardRemove()
    await message.answer(("Напишите название лекарства (Мин: 3 букв)", lang))
    find =+ 1
@dp.message_handler()
async def process_user_medicine(message: types.Message):
 global name1
 global find_manager
 global summa_edit
 global amount_edit
 global last_message
 global infor
 global amount
 edit = 0
 if summa_edit == 1:
       a = message.text + ',00'
       cursor.execute("UPDATE dorilar SET narxi = ? WHERE nomi = ?", (a, name1))
       conn.commit()
       await message.answer(f"Стоимость успешно изменена\nДля выхода с админ режима введите /adminpanel0258off")
       await message.answer(f"Напишите название лекарства для изменения (Мин: 3 букв)")
       summa_edit = 0
       edit = 1
       find_manager = 1
 if amount_edit == 1:
       cursor.execute("UPDATE dorilar SET soni = ? WHERE nomi = ?", (message.text ,name1))
       conn.commit()
       await message.answer(f"Наличие успешно изменена\nДля выхода с админ режима введите /adminpanel0258off")
       await message.answer(f"Напишите название лекарства для изменения (Мин: 3 букв)")
       edit = 1
       find_manager = 1
       amount_edit = 0
 if find_manager == 1:
   if len(message.text) >= 3:
     if message.text[:1] == '🔹':
         name1 = message.text.split('|')[0]
         name1 = name1[1:].strip()
         cursor.execute("SELECT price FROM product_prices WHERE product_name = ?", (name1,))
         infor = cursor.fetchall()
         infor = list(infor[0])
         last_message =  (await message.answer(f"""Лекарство: {name1}
 
 Стоимость: {infor[0]} {("сум", lang)}
 """, reply_markup=keyboard_manager, parse_mode=ParseMode.HTML))
     else:
         user_medicine = message.text
         msg = message.text
         javob = msg
         search_query = (javob(msg).upper())
         cursor.execute("SELECT * FROM product_prices WHERE product_name LIKE ?", (search_query + '%',))
         results = cursor.fetchall()
         keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
         for row in results:
             keyboard.add(KeyboardButton(f'🔹 {row[0]}|💵 {row[1][:-3]} {("сум", lang)}'))
         if edit == 0:
          if results == []:
             await message.answer("Лекарство не найдено 😴")
          else:
             await message.answer("Вот найденные лекарства", reply_markup=keyboard)
         edit = 0
   else:
    try:
     if edit == 0:
        await message.answer(f"Минимум 3 букв")
    except:
        None
 if len(message.text) >= 3:
     if message.text[:1] == '🔹':
         name1 = message.text.split('|')[0]
         name1 = name1[1:].strip()
         cursor.execute("SELECT price FROM product_prices WHERE product_name = ?", (name1,))
         info = cursor.fetchall()
         info = list(info[0])
         global current_value
         current_value = 0
         last_message =  (await message.answer(f"""Лекарство: {name1}
 
 Стоимость: {info[0]}
 ----------------------------------------------------------------------------------------------------
 Есть в аптеках: 
 1) <code>Ташкент, Мирабадский район, массив Госпитальный, 65</code>
 2) <code>41.250756,69.157144, Зангиатинский район, Ташкентская область</code>
 """, reply_markup=keyboards, parse_mode=ParseMode.HTML))
     else:
         user_medicine = message.text
         msg = message.text
         javob = msg
         search_query = (javob(msg).upper())
         cursor.execute("SELECT * FROM product_prices WHERE product_name LIKE ?", (search_query + '%',))
         results = cursor.fetchall()
         keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
         for row in results:

            keyboard.add(KeyboardButton(f'🔹 {row[0]}|💵 {row[1][:-3]} {("сум", lang)}'))
         if results == []:
            await message.answer("Лекарство не найдено 😴")
         else:
            keyboard.add(KeyboardButton(f'⬅️ Назад'))
            await message.answer("Вот найденные лекарства", reply_markup=keyboard)
 else:
       await message.answer(f"Минимум 3 букв")






from keyboards import button_exe
from keyboards import current_value
async def button_ex() -> InlineKeyboardMarkup:
    global current_value
    if current_value > 5:
        keyboards = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton("+10", callback_data='plus10'),InlineKeyboardButton("+", callback_data='plus'),InlineKeyboardButton(f"{current_value}", callback_data="amount"),InlineKeyboardButton("-", callback_data='minus'),InlineKeyboardButton("-10", callback_data='minus10')],
                [InlineKeyboardButton("Добавить в корзину", callback_data='add_cart')]
        ])
    else:
        keyboards = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("+", callback_data='plus'),InlineKeyboardButton(f"{current_value}", callback_data="amount"),InlineKeyboardButton("-", callback_data='minus')],
            [InlineKeyboardButton("Добавить в корзину", callback_data='add_cart')]
    ])
    return keyboards



@dp.callback_query_handler(text="plus")
async def update_button(call: types.CallbackQuery):
    global current_value
    try:
        if int(current_value+1) <= int(amount):
            current_value += 1
        await call.message.edit_reply_markup(reply_markup=await button_ex())
    except:
        None
@dp.callback_query_handler(text="plus10")
async def update_button(call: types.CallbackQuery):
    global current_value,amount
    try:
        if int(current_value+10) <= int(amount):
            current_value += 10
        await call.message.edit_reply_markup(reply_markup=await button_ex())
    except:
        None
@dp.callback_query_handler(text="minus")
async def update_button(call: types.CallbackQuery):
    global current_value
    try:
        if current_value != 0:
            current_value -= 1
        await call.message.edit_reply_markup(reply_markup=await button_ex())
    except:
        None
@dp.callback_query_handler(text="minus10")
async def update_button(call: types.CallbackQuery):
    global current_value
    try:
        if current_value > 10:
            current_value -= 10
        await call.message.edit_reply_markup(reply_markup=await button_ex())
    except:
        None
@dp.callback_query_handler(text="edit_summa")
async def update_button(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.message.chat.id, text='Введите новую цену')
    global summa_edit
    summa_edit = 1
    find_manager = 0
@dp.callback_query_handler(text="edit_amount")
async def update_button(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.message.chat.id, text='Введите новое наличие')
    global amount_edit
    amount_edit = 1
    find_manager = 0
@dp.callback_query_handler(text="add_cart")
async def alert(callback: types.CallbackQuery):
   global cart
   global current_value
   global find
   try:
    if current_value != 0: 
     cursor.execute("SELECT orders FROM users WHERE id = ?", (chat_id,))
     info = list(cursor.fetchall()[0])
     await bot.answer_callback_query(callback.id, text=f'💊{name1}\n{current_value} шт.\n🛒 Добавлен в корзину', show_alert=True)
     cart[name1] = current_value
     find = 0
     print(cart)
     current_value =1
     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
     keyboard.add(KeyboardButton(f'🛒 Корзина'))
     keyboard.add(KeyboardButton(f'🔍 Поиск лекарств'))
     keyboard.add(KeyboardButton(f'⬅️ Назад'))
     await bot.send_message(chat_id=callback.message.chat.id, text="Выберите действие", reply_markup=keyboard)
    else:
     await bot.send_message(chat_id=callback.message.chat.id, text="Нельзя добавить в корзину нулевое значение!")
   except:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(KeyboardButton(f'📞 Дать телефон и местоположение'))
    await bot.send_message(chat_id=callback.message.chat.id, text=" ❌ У вас юнет корзины\nСначала зарегистрируйтесь. Нажмите кнопку ниже ⬇️", reply_markup=keyboard)
    cart = {}
@dp.callback_query_handler(text="buy")
async def update_button(callback: types.CallbackQuery):
    global current_value
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(f'💳 Click (Временно не работает)'))
    keyboard.add(KeyboardButton(f'💵 Наличные'))
    await bot.send_message(chat_id=callback.message.chat.id, text="Выберите способ оплаты", reply_markup=keyboard)
@dp.callback_query_handler(text="delivered")
async def update_button(callback: types.CallbackQuery):
    # Удаляем кнопку, редактируя сообщение и удаляя разметку
    # Получаем номер заказа из callback.data
    message_text = callback.message.text
    order_number = int(message_text.split('|')[1][1:])
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    cursor.execute('SELECT delivered FROM "order" WHERE id_order =?', (order_number,))
    info = list(cursor.fetchall()[0])
    list_data = list(json.loads(info[0]))
    list_data.pop()
    list_data.append("Доставлено")
    json_data1 = json.dumps(list_data)
    # Изменяем статус заказа на "delivered" в базе данных
    cursor.execute('UPDATE "order" SET delivered = ? WHERE id_order = ?', (json_data1, order_number))
    conn.commit()

    # Выводим номер заказа в консоль
    print(f'Заказ {order_number} доставлен')

    # Изменяем текст сообщения на "delivered"
    await bot.send_message(chat_id=callback.message.chat.id,text=f"Заказ {order_number} доставлен")




@dp.callback_query_handler(text="accept")
async def update_button(callback: types.CallbackQuery):
    message = callback.message
    now = datetime.now()
    formatted_date_time = now.strftime("%d:%m:%Y %H:%M")
    keyboards = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(f"✅ Доставлено", callback_data='delivered')]])
    cursor.execute("SELECT cord FROM users WHERE id = ?", (chat_id,))
    cord_txt = cursor.fetchall()
    cord_txt = list(cord_txt[0])
    cord = list(json.loads(cord_txt[0]))
    location = types.Location(latitude=cord[0], longitude=cord[1])
    await bot.send_message(MANAGER_USER_ID,f"""Заказ:|№
--------------------------------
💊 Лекарства:
{cart_info}
--------------------------------
💲Оплата: {formatted_total}{("сум", lang)}
{sposob_oplati}
--------------------------------
📍 Адрес: {address}
{delivery_info}
--------------------------------
ℹ️ Данные клиента:
🆔 Username: @{usernam}
📞 Телефон номер: <code>+{phone_number}</code>
--------------------------------
🗓 Дата {formatted_date_time}
            ⬇️⬇️⬇️ Местоположение ⬇️⬇️⬇️
    """, parse_mode=ParseMode.HTML, reply_markup=keyboards)
    await bot.send_location(
        MANAGER_USER_ID,
        location.latitude,
        location.longitude)
    await bot.send_message(MANAGER_USER_ID, text=f"⬆️⬆️⬆️ Местоположение ⬆️⬆️⬆️")
    list_data = []
    list_data.append(usernam)
    list_data.append(phone_number)
    # Сериализуем список в JSON
    json_data1 = json.dumps(list_data)
    list_data = []
    list_data.append(delivery_info)
    list_data.append('Доставляется')
    # Сериализуем список в JSON
    json_data2 = json.dumps(list_data)
    cursor.execute('INSERT INTO "order" VALUES (?,?,?,?,?,?,?)', (nom, cart_info, formatted_total, address,json_data1, json_data2, formatted_date_time))
    cursor.execute("SELECT orders FROM users WHERE id = ?", (chat_id,))
    info = list(cursor.fetchall()[0])
    # Строка JSON
    json_data = info[0]
    # Десериализуем строку JSON обратно в список
    try:
        list_data = list(json.loads(json_data))
    except:
        list_data = []
    # Вывод: [1, 2, 3, 4, 5]
    # Создаем список
    list_data.append(nom)
    # Сериализуем список в JSON
    json_data = json.dumps(list_data)
    # Вывод: "[1, 2, 3, 4, 5]"

    cursor.execute("UPDATE users SET orders = ? WHERE id = ?", (json_data, chat_id))
    await bot.send_message(chat_id=callback.message.chat.id, text="Sizning buyurtmangiz qabul qilindi, manager javobini kutib qoling")
    conn.commit()
    global cart
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    items = cart.items()
    for i in items:
        cursor.execute("SELECT soni FROM dorilar WHERE nomi = ?", (i[0],))
        soni = cursor.fetchall()
        soni = list(soni[0])
        soni = int(soni[0].replace(",", "")) - int(i[1])
        cursor.execute("UPDATE dorilar SET soni =? WHERE nomi =?", (soni, i[0]))
        conn.commit()


    cart = {}
    keyboard.add(KeyboardButton(f'👤 Profil'))
    keyboard.add(KeyboardButton(f'🔍 Dori-darmon qidirish'))

    await bot.send_message(chat_id=callback.message.chat.id, text="Amalni tanlang", reply_markup=keyboard)





@dp.message_handler(commands=['my_chat_id'])
async def get_chat_id(message: types.Message):
    chat_id = message.chat.id
    await message.answer(f"Chat ID этой группы успешно сохранена")



if __name__ == '__main__':
    while True:
        try:
            executor.start_polling(dp, skip_updates=True)
        except Exception as e:
            print(f'Ошибка: {e}.\nПерезапуск бота через 10 секунд.')
            time.sleep(10)