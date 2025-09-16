from datetime import date, datetime
import random
import webbrowser
from aiogram import Bot, types
from aiogram import Dispatcher
import aiogram.types
from aiogram.utils import executor
from A import TOKEN1
from aiogram.types import Message
import logging

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN1)
dp = Dispatcher(bot)

product_prices = {
    'Anor': {'price' :18000, 'link_p':"https://gardencells.com/files/original/products/68.jpg"},
    'Shaptoli': {'price' :15000, 'link_p':"https://agri-gator.com.ua/wp-content/uploads/2021/10/nektarin.jpg"},
    'Olma': {'price' :15000, 'link_p':"https://srcyrl.bestplanthormones.com/Content/upload/2019264467/201906051807366069299.jpg"},
    'Nok': {'price' :15000, 'link_p':"https://zira.uz/wp-content/uploads/2018/09/int-fakti-grusha-2.jpg"},
    'Muzqaymoq': {'price' :65000, 'link_p':"https://uzreport.news/fotobank/image/3e23bbac36894a1a4627d7464108240e.jpeg"},
    'Qurt': {'price' :82000, 'link_p':"https://shop.chuztrade.uz/wp-content/uploads/2018/12/9565f4e6d2a4207358f54.jpg"},
    'Qaymoq': {'price' :10000, 'link_p':"https://yukber.uz/image/cache/catalog/smetana-23-700x700.jpg"},
    'Sut': {'price' :11000, 'link_p':"https://yuz.uz/imageproxy/1200x/https://yuz.uz/file/news/918e89a4acbb413819949216503353ab.jpg"},
    'Mol go`shti': {'price' :90000, 'link_p':"https://zamin.uz/uploads/posts/2017-06/1497253009_593d4f6cbe33c.jpg"},
    "Sabzi": {'price' :11000, 'link_p':"https://storage.kun.uz/source/7/SBpc8GysM0sg0bGCTLm4tBn760-w5l6w.jpg"},
    "Bodring": {'price' :11000, 'link_p':"https://www.spot.uz/media/img/2023/11/TfxzIc17010644618077_l.jpg"},
    "Pamidor": {'price' :12000, 'link_p':"https://stat.uz/images/aaacfisj9wtznmregenojdxxt8d2zlc1vp4phnpzdacxirhjtt4kvfbdaiwcno-_p79984.jpg"},
    "Kartoshka": {'price' :7000, 'link_p':"https://www.belta.by/images/storage/news/with_archive/2023/000029_1686923312_572263_big.jpg"},
    'Tovuq go`shti': {'price' :80000, 'link_p':"https://dostavo4ka.uz/upload-file/2021/05/05/2432/c957b80b-43ba-443b-9aba-8b2c5b946541.jpg"},
    'Qo`y go`shti': {'price' :70000, 'link_p':"https://chakchak.uz/uploads/images/tips/7c5dabc875cdcda3.jpg"},
    'Qiyma go`shti': {'price' :77000, 'link_p':"https://dostavo4ka.uz/upload-file/2021/05/05/3386/750x750-0a3e03ed-23e5-4279-8a7b-318421786aeb.jpg"},
    'Marmelad': {'price' :75000, 'link_p':"https://www.zefir.by/upload/iblock/b03/b030f280c5e885afc7725bb2b3da357b.png"},
    'Pechenye': {'price' :68000, 'link_p':"https://www.vkusnyblog.com/wp-content/uploads/2015/02/pechenye-s-shokoladom.jpg"},
    'Cheers': {'price' :9000, 'link_p':"https://dostavo4ka.uz/upload-file/2021/05/05/2608/5e828945-1e92-49b0-8458-b174bd65a162.jpg"},
    'Snickers': {'price' :7000, 'link_p':"https://aquamarket.ua/25109-large_default/snickers-upakovka-40-sht-po-50-g-shokoladnye-batonchiki-snikers.jpg"},
    'Non': {'price' :5000, 'link_p':"https://www.shutterstock.com/image-photo/tandir-non-lepeshka-tarditional-uzbek-260nw-1425851096.jpg"}   
}

answers = ['Не понял, что вы сказали.', 'Извините, я вас не понял.', 'Не знаю, что делать с такой командой.', 'Мой программист не научил меня отвечать на это... >_<']
answers1 = ["Этот товар появится как можно скоро", "Этот товар в настоящее время не продается"]
img = "images/anor.png"
counter_dict = {}

@dp.message_handler(commands=['start'])
async def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🛒 Товары')
    button2 = types.KeyboardButton('⚙️ Настройки')
    button3 = types.KeyboardButton('📄 Помощь')
    markup.row(button1)
    markup.row(button2, button3)
    counter_dict[message.chat.id] = 0

    if message.text == '/start':
        now = datetime.now().strftime("%H:%M:%S")
        if now < "12:00:00": 
            await bot.send_message(message.chat.id, f"""Доброе утро, {message.from_user.first_name}!\nЧерез меня вы можете приобрести некоторые товары!""", reply_markup=markup)
        elif now >= "12:00:00" and now < "18:00:00":
             await bot.send_message(message.chat.id, f"""Добрый день, {message.from_user.first_name}!\nЧерез меня вы можете приобрести некоторые товары!""", reply_markup=markup)
        else:
            await bot.send_message(message.chat.id,f"""Добрый вечер, {message.from_user.first_name}!\nЧерез меня вы можете приобрести некоторые товары!""", reply_markup=markup)
    else:
        await bot.send_message(message.chat.id, "Перехожу в основное меню! Выберите!", reply_markup=markup)

@dp.message_handler(content_types='photo')
async def get_photo(message):
    await bot.send_message(message.chat.id, 'Извините, но просмотр фотографий не поддерживается. :(')

@dp.message_handler()
async def info(message):
    if message.text == '🛒 Товары':
        await categories(message)
    elif message.text == '⚙️ Настройки':
        await settingsChapter(message)
    elif message.text == "🗓 Категория":
       await categories(message)
    elif message.text == '📄 Помощь':
        await infoChapter(message)
    elif message.text == "Стрейч":
        await strich(message)
    elif message.text == "🥕 Sabzavotlar":
        await vegetables(message)
    # elif message.text == "🥛 Sut mahsulotlari":
    #     await milk_products(message)
    elif message.text == "🥩 Go`sht":
        await meat(message)
    elif message.text == "🥗 Boshqa mahsulotlar":
        await other_products(message)
    elif message.text == '🔹 Anor':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Sotib olish')
        button2 = types.KeyboardButton('↩️ Orqaga')
        markup.row(button1, button2)
        photo_url = "https://gardencells.com/files/original/products/68.jpg"
        caption = """Anor haqida ma'lumot:
    Narxi:18000 so'm/kg"""
        await bot.send_photo(message.chat.id, photo=photo_url, caption=caption, reply_markup=markup)
        # async def send_photo(message: types.Message):
        # await bot.send_photo(message.chat.id, photo=photo_url, caption=caption, reply_markup=markup)
        #         image_url = ("images/anor.png")
        #         caption = 'Birinchi mahsulot haqida ma\'lumot...'
        #         await bot.send_photo(message.chat.id, image_url, caption=caption, parse_mode=ParseMode.MARKDOWN)
    elif message.text == '🛍 Пакеты':
        # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # button1 = types.KeyboardButton('Подарочные пакеты')
        # button2 = types.KeyboardButton('Полиэтиленовые пакеты')
        # button3 = types.KeyboardButton('Крафт пакеты')
        # button4 = types.KeyboardButton('Мусорные пакеты')
        # markup.row(button1, button2)
        # markup.row(button3, button4)
        await packets(message)
    elif message.text == '🔹 Shaptoli':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Sotib olish')
        button2 = types.KeyboardButton('↩️ Orqaga')
        markup.row(button1, button2)
        photo_url = "https://agri-gator.com.ua/wp-content/uploads/2021/10/nektarin.jpg"
        caption = """Shaptoli haqida ma'lumot:
    Narxi:15000 so'm/kg"""

        await bot.send_photo(message.chat.id, photo=photo_url, caption=caption, reply_markup=markup)
    elif message.text == '🔹 Muzqaymoq':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Sotib olish')
        button2 = types.KeyboardButton('↩️ Orqaga')
        markup.row(button1, button2)
        photo_url = "https://uzreport.news/fotobank/image/3e23bbac36894a1a4627d7464108240e.jpeg"
        caption = """Muzqaymoq haqida ma'lumot:
    Narxi:88000 so'm/kg"""
        await bot.send_photo(message.chat.id, photo=photo_url, caption=caption, reply_markup=markup)
    elif message.text == '🔹 Cheers':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Sotib olish')
        button2 = types.KeyboardButton('↩️ Orqaga')
        markup.row(button1, button2)
        photo_url = "https://dostavo4ka.uz/upload-file/2021/05/05/2608/5e828945-1e92-49b0-8458-b174bd65a162.jpg"
        caption = """Cheers haqida ma'lumot:
    Narxi:9000 so'm/dona"""
        await bot.send_photo(message.chat.id, photo=photo_url, caption=caption, reply_markup=markup)
    elif message.text == '🔹 Snickers':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Sotib olish')
        button2 = types.KeyboardButton('↩️ Orqaga')
        markup.row(button1, button2)
        photo_url = "https://aquamarket.ua/25109-large_default/snickers-upakovka-40-sht-po-50-g-shokoladnye-batonchiki-snikers.jpg"
        caption = """Snickers haqida ma'lumot:
    Narxi:7000 so'm/dona"""
        await bot.send_photo(message.chat.id, photo=photo_url, caption=caption, reply_markup=markup)
    elif message.text == '🔹 Non':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Sotib olish')
        button2 = types.KeyboardButton('↩️ Orqaga')
        markup.row(button1, button2)
        photo_url = "https://www.shutterstock.com/image-photo/tandir-non-lepeshka-tarditional-uzbek-260nw-1425851096.jpg"
        caption = """Non haqida ma'lumot:
    Narxi:5000 so'm/dona"""
        await bot.send_photo(message.chat.id, photo=photo_url, caption=caption, reply_markup=markup)
    elif message.text == '🔹 Pamidor':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Sotib olish')
        button2 = types.KeyboardButton('↩️ Orqaga')
        markup.row(button1, button2)
        photo_url = "https://stat.uz/images/aaacfisj9wtznmregenojdxxt8d2zlc1vp4phnpzdacxirhjtt4kvfbdaiwcno-_p79984.jpg"
        caption = """Pamidor haqida ma'lumot:
    Narxi:12000 so'm/kg"""
        await bot.send_photo(message.chat.id, photo=photo_url, caption=caption, reply_markup=markup)
    elif message.text == '🔹  #9':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Sotib olish')
        button2 = types.KeyboardButton('↩️ Orqaga')
        markup.row(button1, button2)
        photo_url = "https://uzreport.news/fotobank/image/3e23bbac36894a1a4627d7464108240e.jpeg"
        caption = """Snickers haqida ma'lumot:
    Narxi:7000 so'm/200g"""
        await bot.send_photo(message.chat.id, photo=photo_url, caption=caption, reply_markup=markup)
    elif message.text == '🔹 Nok':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Sotib olish')
        button2 = types.KeyboardButton('↩️ Orqaga')
        markup.row(button1, button2)
        photo_url = "https://zira.uz/wp-content/uploads/2018/09/int-fakti-grusha-2.jpg"
        caption = """Nok haqida ma'lumot:
    Narxi:15000 so'm/kg"""
        await bot.send_photo(message.chat.id, photo=photo_url, caption=caption, reply_markup=markup)
    elif message.text == '🔹 Olma':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Sotib olish')
        button2 = types.KeyboardButton('↩️ Orqaga')
        markup.row(button1, button2)
        photo_url = "https://srcyrl.bestplanthormones.com/Content/upload/2019264467/201906051807366069299.jpg"
        caption = """Olma haqida ma'lumot:
    Narxi:15000 so'm/kg"""
        await bot.send_photo(message.chat.id, photo=photo_url, caption=caption, reply_markup=markup)
    elif message.text == '🔹 Qaymoq':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Sotib olish')
        button2 = types.KeyboardButton('↩️ Orqaga')
        markup.row(button1, button2)
        photo_url = "https://yukber.uz/image/cache/catalog/smetana-23-700x700.jpg"
        caption = """Qaymoq haqida ma'lumot:
    Narxi:10000 so'm/250gram"""
        await bot.send_photo(message.chat.id, photo=photo_url, caption=caption, reply_markup=markup)
    elif message.text == '🔹 Sut':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Sotib olish')
        button2 = types.KeyboardButton('↩️ Orqaga')
        markup.row(button1, button2)
        photo_url = "https://yuz.uz/imageproxy/1200x/https://yuz.uz/file/news/918e89a4acbb413819949216503353ab.jpg"
        caption = """Sut haqida ma'lumot:
    Narxi:11000 so'm/500ml"""
    elif message.text == '🔹 Sabzi':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Sotib olish')
        button2 = types.KeyboardButton('↩️ Orqaga')
        markup.row(button1, button2)
        photo_url = "https://storage.kun.uz/source/7/SBpc8GysM0sg0bGCTLm4tBn760-w5l6w.jpg"
        caption = """Sut haqida ma'lumot:
    Narxi:11000 so'm/500ml"""
    elif message.text == '🔹 Bodring':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Sotib olish')
        button2 = types.KeyboardButton('↩️ Orqaga')
        markup.row(button1, button2)
        photo_url = "https://www.spot.uz/media/img/2023/11/TfxzIc17010644618077_l.jpg"
        caption = """Sut haqida ma'lumot:
    Narxi:11000 so'm/500ml"""
    elif message.text == '🔹 Kartoshka':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Sotib olish')
        button2 = types.KeyboardButton('↩️ Orqaga')
        markup.row(button1, button2)
        photo_url = "https://www.belta.by/images/storage/news/with_archive/2023/000029_1686923312_572263_big.jpg"
        caption = """Sut haqida ma'lumot:
    Narxi:11000 so'm/500ml"""
        await bot.send_photo(message.chat.id, photo=photo_url, caption=caption, reply_markup=markup)
    elif message.text == "30 см":
        await send_third_set(message)
        await send_second_set(message)
        await send_first_set(message)
        await send_photo_set(message)
        await send_photo_set2(message)
        await send_photo_set3(message)
        await send_photo_set4(message)
    elif message.text == "45 см":
        photo_url = ["Python\images\photo_2024-01-11_21-40-26.jpg", "Python\images\photo_2024-01-11_21-40-29.jpg", "Python\images\photo_2024-01-11_21-40-31.jpg"]
        media = [types.InputMediaPhoto(media=open(photo, 'rb')) for photo in photo_url]
        media[0].caption = '70000 сум/шт'
        await bot.send_media_group(message.chat.id, media)


    elif message.text == "🌐 Изменить язык":
        await language(message)
    elif message.text == '✏️ Написать разработчику':
        await bot.send_message(message.chat.id, "https://t.me/Jas_623007")
        await bot.send_message(message.chat.id, "https://t.me/Jorayev_Behruz")
    elif message.text == "📄 Справка":
        await reference(message)
    elif message.text == '↩️ Назад':
        await categories(message)
    elif message.text == '↩️ Вернуться назад':
        await pay_for(message)
    elif message.text == '↩️ Вернуться в меню':
         await welcome(message)
    elif message.text == "👈 Назад":
         await settingsChapter(message)
    elif message.text == '💳 Купить':
         await increase_decrease(message)
    elif message.text == "+":
        counter_dict[message.chat.id] += 1
        await bot.send_message(message.chat.id,f'{counter_dict[message.chat.id]}dona/kilo')
    elif message.text == '-' and counter_dict[message.chat.id] > 1:
        counter_dict[message.chat.id] -= 1
        await bot.send_message(message.chat.id, f'{counter_dict[message.chat.id]}dona/kilo')
    elif message.text == '-' and counter_dict[message.chat.id] == 1:
        await bot.send_message(message.chat.id, '1kilodan kam bolishi mumkun emas')
    elif message.text == "💳 Оплатить":
        await pay_for(message)
    elif message.text == "💸 Наличные":
        await order(message)
    elif message.text == "💳 Картой":
        await order(message)
        await bot.send_message(message.chat.id, "Введите номер вашей карты:⬇️⬇️⬇️")
    elif message.text == "🚚 Заказать":
        await bot.send_message(message.chat.id, "Благодарим вас за заказ!!!😊")
        await categories(message)
    elif message.text == "➕ Добавить товары":
        await categories(message)
    elif message.text == "80 см":
        await bot.send_message(message.chat.id, answers1[random.randint(0, 1)])
    else:
        await bot.send_message(message.chat.id, answers[random.randint(0, 3)])


async def categories(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Стрейч')
    button2 = types.KeyboardButton('')
    button3 = types.KeyboardButton('Фольга')
    button4 = types.KeyboardButton("🛍 Пакеты")
    button5 = types.KeyboardButton("🍽 Одноразовые посуды")
    button7 = types.KeyboardButton("🥣 Контейнеры")
    button6 = types.KeyboardButton('↩️ Вернуться в меню')
    markup.row(button1, button2)
    markup.row(button3, button4)
    markup.row(button5, button7)
    markup.row(button6)
    await bot.send_message(message.chat.id, 'Все товары, которые есть в продаже:', reply_markup=markup)

async def packets(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('Подарочные пакеты')
        button2 = types.KeyboardButton('Полиэтиленовые пакеты')
        button3 = types.KeyboardButton('Крафт пакеты')
        button4 = types.KeyboardButton('Мусорные пакеты')
        button5 = types.KeyboardButton('🗓 Категория')
        markup.row(button1, button2)
        markup.row(button3, button4)
        markup.row(button5)
        await bot.send_message(message.chat.id, "Вы выбрали пакеты:", reply_markup=markup)

async def strich(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('30 см')
    button2 = types.KeyboardButton('45 см')
    button4 = types.KeyboardButton('80 см')
    button5 = types.KeyboardButton('🗓 Категория')
    markup.row(button5)
    markup.row(button1, button2)
    markup.row(button4)
    await bot.send_message(message.chat.id, "Вы выбрали стрейч:", reply_markup=markup)
    
async def vegetables(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🔹 Pamidor')
    button2 = types.KeyboardButton('🔹 Sabzi')
    button3 = types.KeyboardButton('🔹 Bodring')
    button4 = types.KeyboardButton('🔹 Kartoshka')
    button5 = types.KeyboardButton('🗓 Категория')
    markup.row(button5)
    markup.row(button1, button2)
    markup.row(button3, button4)
    await bot.send_message(message.chat.id, 'Все товары, которые есть в продаже:', reply_markup=markup)
    
async def meat(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🔹 Mol go`shti')
    button2 = types.KeyboardButton('🔹 Tovuq go`shti')
    button3 = types.KeyboardButton('🔹 Qo`y go`shti')
    button4 = types.KeyboardButton('🔹 Qiyma go`sh')
    button5 = types.KeyboardButton('🗓 Категория')
    markup.row(button5)
    markup.row(button1, button2)
    markup.row(button3, button4)
    await bot.send_message(message.chat.id, 'Все товары, которые есть в продаже:', reply_markup=markup)
    
async def other_products(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🔹 Cheers')
    button2 = types.KeyboardButton('🔹 Snickers')
    button3 = types.KeyboardButton('🔹 Marmelad')
    button4 = types.KeyboardButton('🔹 Pechenye')
    button5 = types.KeyboardButton('🗓 Kategoriya')
    markup.row(button5)
    markup.row(button1, button2)
    markup.row(button3, button4)
    await bot.send_message(message.chat.id, 'Все товары, которые есть в продаже:', reply_markup=markup)

async def settingsChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("🌐 Изменить язык")
    button3 = types.KeyboardButton('↩️ Вернуться в меню')
    markup.row(button1, button3)
    await bot.send_message(message.chat.id, 'Настройки.\nВыберите один из вариантов:', reply_markup=markup)


async def infoChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('✏️ Написать разработчику')
    button2 = types.KeyboardButton('↩️ Вернуться в меню')
    button3 = types.KeyboardButton("📄 Справка")
    markup.row(button1, button3)
    markup.row(button2)
    await bot.send_message(message.chat.id, 'Справка.\nЗдесь вы можете отправить сообщение разработчику.', reply_markup=markup)

async def increase_decrease(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 =  types.KeyboardButton('+')
    button2 =  types.KeyboardButton('-')
    button3 =  types.KeyboardButton('↩️ Orqaga')
    button4 = types.KeyboardButton("💳 To'lash")
    button5 = types.KeyboardButton("➕ Mahsulotlar qo'shish")
    markup.row(button1, button2)
    markup.row(button3, button4)
    markup.row(button5)
    await bot.send_message(message.chat.id, 'Necha kilo olmoqchisiz?', reply_markup=markup)

async def send_photos(message: types.Message, photo_paths, captions):
    media = [types.InputMediaPhoto(media=open(photo, 'rb'), caption=captions[i]) for i, photo in enumerate(photo_paths)]
    await bot.send_media_group(message.chat.id, media)

async def send_first_set(message: types.Message):
    photo_paths = ["Python\images\photo_2024-01-11_21-38-16.jpg", "Python\images\photo_2024-01-11_21-38-20.jpg", "Python\images\photo_2024-01-11_21-38-22.jpg"]
    media = [types.InputMediaPhoto(media=open(photo, 'rb')) for photo in photo_paths]
    media[0].caption = '7500 сум/шт'
    await bot.send_media_group(message.chat.id, media)

async def send_second_set(message: types.Message):
    photo_paths = ["Python\images\photo_2024-01-11_21-38-24.jpg", "Python\images\photo_2024-01-11_21-39-20.jpg", "Python\images\photo_2024-01-11_21-39-28.jpg"]
    media = [types.InputMediaPhoto(media=open(photo, 'rb')) for photo in photo_paths]
    media[0].caption = '8500 сум/шт'
    await bot.send_media_group(message.chat.id, media)

async def send_third_set(message: types.Message):
    photo_paths = ["Python\images\photo_2024-01-11_21-39-52.jpg", "Python\images\photo_2024-01-11_21-39-55.jpg", "Python\images\photo_2024-01-11_21-39-57.jpg"]
    media = [types.InputMediaPhoto(media=open(photo, 'rb')) for photo in photo_paths]
    media[0].caption = '5500 сум/шт'
    await bot.send_media_group(message.chat.id, media)

async def pay_for(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("💸 Наличные")
    button2 = types.KeyboardButton("💳 Картой")
    button3 = types.KeyboardButton("↩️ Назад")
    markup.row(button1,button2)
    markup.row(button3)
    await bot.send_message(message.chat.id, "Выберите метод оплаты💸:", reply_markup=markup)

async def order(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("🚚 Заказать")
    button2 = types.KeyboardButton("↩️ Вернуться назад")
    markup.row(button1)
    markup.row(button2)
    await bot.send_message(message.chat.id, "⬇️⬇️⬇️", reply_markup=markup)
async def language(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("🇺🇿 O'zbekcha")
    button2 = types.KeyboardButton('🇷🇺 Русский')
    button4 = types.KeyboardButton('👈 Orqaga')
    markup.row(button1,button2)
    markup.row(button4)
    await bot.send_message(message.chat.id, f"Tilni tanlang:", reply_markup=markup)
    
async def send_photo_set(message: types.Message):
    photo_paths = ["Python\images\photo_2024-01-11_21-39-31.jpg", "Python\images\photo_2024-01-11_21-39-34.jpg", "Python\images\photo_2024-01-11_21-39-36.jpg"]
    media = [types.InputMediaPhoto(media=open(photo, 'rb')) for photo in photo_paths]
    media[0].caption = '9500 сум/шт'
    await bot.send_media_group(message.chat.id, media)

async def send_photo_set2(message: types.Message):
    photo_paths = ["Python\images\photo_2024-01-11_21-39-43.jpg", "Python\images\photo_2024-01-11_21-39-47.jpg", "Python\images\photo_2024-01-11_21-39-50.jpg"]
    media = [types.InputMediaPhoto(media=open(photo, 'rb')) for photo in photo_paths]
    media[0].caption = '25000 сум/шт'
    await bot.send_media_group(message.chat.id, media)

async def send_photo_set3(message: types.Message):
    photo_paths = ["Python\images\photo_2024-01-11_21-40-03.jpg", "Python\images\photo_2024-01-11_21-40-06.jpg", "Python\images\photo_2024-01-11_21-40-08.jpg"]
    media = [types.InputMediaPhoto(media=open(photo, 'rb')) for photo in photo_paths]
    media[0].caption = '5000 сум/шт'
    await bot.send_media_group(message.chat.id, media)

async def send_photo_set4(message: types.Message):
    photo_paths = ["Python\images\photo_2024-01-11_21-40-16.jpg", "Python\images\photo_2024-01-11_21-40-19.jpg", "Python\images\photo_2024-01-11_21-40-22.jpg"]
    media = [types.InputMediaPhoto(media=open(photo, 'rb')) for photo in photo_paths]
    media[0].caption = '25000 сум/шт'
    await bot.send_media_group(message.chat.id, media)


async def reference(message):
    await bot.send_message(message.chat.id, f"""Bizning botimiz haqida:
    Date of release:18.11.2023
    Version:2.2
    Last update:07.01.2024
    Developers:Behruz Jo'rayev
    Jasurbek Zokirov""")

if __name__ == '__main__':
    executor.start_polling(dp)
    
# 🍅🍞🍫🍟🍨🍑🍈🥭