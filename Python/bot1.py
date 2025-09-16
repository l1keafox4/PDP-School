from datetime import date, datetime
import random
import webbrowser
from aiogram import Bot, types, Dispatcher
import aiogram.types
from aiogram.utils import executor
from c import TOKEN
from aiogram.types import Message
import logging

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

Lox = {}

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
chosen_products = {}
answers = ['Men nima deganingizni tushunmadim.', 'Kechirasiz, sizni tushunmadim.', 'Bunday buyruqni bilmayman.', 'Mening dasturchim bu holatda javob berishni aytgan emas... >_<']
img = "images/anor.png"
counter_dict = {}
# @dp.message_handler(commands=['info'])
# async def info(message):
#     user_id = message.chat.id
#     if user_id < len(chosen_products):
#         product_name = chosen_products[user_id]
#         await bot.send_message(user_id, f"Chosen product: {product_name}")
#     else:
#         await bot.send_message(user_id, "You haven't chosen any product yet.")

# @dp.message_handler(commands=['cart'])
# async def view_cart(message):
#     user_id = message.chat.id

#     if user_id in chosen_products_dict:
#         total_cart_price = sum([item['total_price'] for item in chosen_products_dict[user_id].values()])
#         cart_info = [f"{item['name']} - {item['quantity']} dona/kilo: {item['total_price']} so'm" for item in chosen_products_dict[user_id].values()]



#         await bot.send_message(user_id, f"🛒 Tanlangan mahsulotlar:\n\n" + '\n'.join(cart_info) + f"\n\nJami summa: {total_cart_price} so'm")
#     else:
#         await bot.send_message(user_id, "Siz hali hech qanday mahsulot tanlamadingiz.")

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in Lox:
        Lox[user_id] = {'first_name': message.from_user.first_name, 'start_time': datetime.now()}
        
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🛍 Mahsulotlar')
    button2 = types.KeyboardButton('⚙️ Sozlamalar')
    button3 = types.KeyboardButton('📄 Yordam')
    markup.row(button1)
    markup.row(button2, button3)
    counter_dict[message.chat.id] = 0

    now = datetime.now().strftime("%H:%M:%S")
    greeting = ""
    
    if now < "12:00:00": 
        greeting = f"Hayrli tong, {message.from_user.first_name}!\nMen orqali siz ba'zi mahsulotlarni sotib olishingiz mumkin!"
    elif now >= "12:00:00" and now < "18:00:00":
        greeting = f"Hayrli kun, {message.from_user.first_name}!\nMen orqali siz ba'zi mahsulotlarni sotib olishingiz mumkin!"
    else:
        greeting = f"Hayrli kech, {message.from_user.first_name}!\nMen orqali siz ba'zi mahsulotlarni sotib olishingiz mumkin!"

    await bot.send_message(message.chat.id, greeting, reply_markup=markup)
    # else:
    #     await bot.send_message(message.chat.id, "Sizni asosiy menyuga o'tkazdim! Tanlang!", reply_markup=markup)

@dp.message_handler(content_types='photo')
async def get_photo(message):
    await bot.send_message(message.chat.id, 'Rasmni ko\'rishim mumkin emas :(')

@dp.message_handler()
async def info(message):
    if message.text == '🛍 Mahsulotlar':
        await categories(message)
    elif message.text == '⚙️ Sozlamalar':
        await settingsChapter(message)
    elif message.text == "🗓 Kategoriya":
       await categories(message)
    elif message.text == '📄 Yordam':
        await infoChapter(message)
    elif message.text == "🍏 Mevalar":
        await fruit(message)
    elif message.text == "🥕 Sabzavotlar":
        await vegetables(message)
    elif message.text == "🥛 Sut mahsulotlari":
        await milk_products(message)
    elif message.text == "🥩 Go`sht":
        await meat(message)
    elif message.text == "🥗 Boshqa mahsulotlar":
        await other_products(message)
    elif message.text == '🔹 Anor':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Sotib olish')
        button2 = types.KeyboardButton('↩️ Orqaga')
        markup.row(button1, button2)
        photo_url = f"{product_prices['Anor']['link_p']}"
        
        caption = f"""Anor haqida ma'lumot:
    Narxi: {product_prices['Anor']['price']} so'm/kg"""
        
        await bot.send_photo(message.chat.id, photo=photo_url, caption=caption, reply_markup=markup)
        # with open(photo_url, 'rb') as photo:
        #     await bot.send_photo(message.chat.id, photo, caption=caption, reply_markup=markup)
        # async def send_photo(message: types.Message):
        # await bot.send_photo(message.chat.id, photo=photo_url, caption=caption, reply_markup=markup)
        #         image_url = ("images/anor.png")
        #         caption = 'Birinchi mahsulot haqida ma\'lumot...'
        #         await bot.send_photo(message.chat.id, image_url, caption=caption, parse_mode=ParseMode.MARKDOWN)
    elif message.text == '🔹 Qurt':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Sotib olish')
        button2 = types.KeyboardButton('↩️ Orqaga')
        markup.row(button1, button2)
        photo_url = f"{product_prices['Qurt']['link_p']}"
        caption = f"""Qurt haqida ma'lumot:
    Narxi:{product_prices['Qurt']['price']} so'm/kg"""
        await bot.send_photo(message.chat.id, photo=photo_url, caption=caption, reply_markup=markup)
    elif message.text == '🔹 Shaptoli':

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Sotib olish')
        button2 = types.KeyboardButton('↩️ Orqaga')
        markup.row(button1, button2)
        photo_url = f"{product_prices['Shaptoli']['link_p']}"
        caption = f"""Shaptoli haqida ma'lumot:
    Narxi:{product_prices['Shaptoli']['price']} so'm/kg"""

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
    elif message.text == "🌐 Tilni o'zgartirish":
        await language(message)
    elif message.text == '✏️ Dasturchiga yozish':
        await bot.send_message(message.chat.id,f"{'https://t.me/Jas_623007'}")
        await bot.send_message(message.chat.id,f"{'https://t.me/Jorayev_Behruz'}")
    elif message.text == "📄 Ma'lumotnoma":
        await reference(message)
    elif message.text == '↩️ Orqaga':
        await categories(message)
    elif message.text == '↩️ Orqaga qaytish':
        await pay_for(message)
    elif message.text == '↩️ Menyuga qaytish':
         await welcome(message)
    elif message.text == "👈 Orqaga":
         await settingsChapter(message)
    elif message.text == '💳 Sotib olish':
         await increase_decrease(message)
    elif message.text == '-' and counter_dict[message.chat.id] == 1:
        await bot.send_message(message.chat.id, '1kilodan kam bolishi mumkun emas')
    elif message.text == "💳 To'lash":
        await pay_for(message)
    elif message.text == "💸 Naqd pul":
        await order(message)
    elif message.text == "💳 Karta orqali":
        await order(message)

        await bot.send_message(message.chat.id,"Kartangizni raqamini yozing:⬇️⬇️⬇️")
    elif message.text == "🚚 Buyurtma berish":
        # await bot.send_message(message.chat.id,"Buyurtmalar imkon qadar tezroq paydo bo'ladi")
        await bot.send_message(message.chat.id,"Buyurtmangiz uchun raxmat!!!😊")
        await categories(message)
    elif message.text == "➕ Mahsulotlar qo'shish":
        await categories(message)
    else:
        await bot.send_message(message.chat.id, answers[random.randint(0, 3)])

async def categories(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🍏 Mevalar')
    button2 = types.KeyboardButton('🥕 Sabzavotlar')
    button3 = types.KeyboardButton('🥛 Sut mahsulotlari')
    button4 = types.KeyboardButton("🥩 Go`sht")
    button5 = types.KeyboardButton("🥗 Boshqa mahsulotlar")
    button6 = types.KeyboardButton('↩️ Menyuga qaytish')
    markup.row(button1, button2)
    markup.row(button3, button4)
    markup.row(button5)
    markup.row(button6)
    await bot.send_message(message.chat.id, 'Hozir sotuvda bo\'lgan barcha mahsulotlar:', reply_markup=markup)

async def fruit(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🔹 Anor')
    button3 = types.KeyboardButton('🔹 Shaptoli')
    button2 = types.KeyboardButton('🔹 Olma')
    button4 = types.KeyboardButton('🔹 Nok')
    button5 = types.KeyboardButton('🗓 Kategoriya')
    markup.row(button5)
    markup.row(button1, button2)
    markup.row(button3, button4)
    await bot.send_message(message.chat.id, 'Hozir sotuvda bo\'lgan barcha mahsulotlar:', reply_markup=markup)
    
async def milk_products(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🔹 Muzqaymoq')
    button2 = types.KeyboardButton('🔹 Qurt')
    button3 = types.KeyboardButton('🔹 Qaymoq')
    button4 = types.KeyboardButton('🔹 Sut')
    button5 = types.KeyboardButton('🗓 Kategoriya')
    markup.row(button5)
    markup.row(button1, button2)
    markup.row(button3, button4)
    await bot.send_message(message.chat.id, 'Hozir sotuvda bo\'lgan barcha mahsulotlar:', reply_markup=markup)
    
async def vegetables(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🔹 Pamidor')
    button2 = types.KeyboardButton('🔹 Sabzi')
    button3 = types.KeyboardButton('🔹 Bodring')
    button4 = types.KeyboardButton('🔹 Kartoshka')
    button5 = types.KeyboardButton('🗓 Kategoriya')
    markup.row(button5)
    markup.row(button1, button2)
    markup.row(button3, button4)
    await bot.send_message(message.chat.id, 'Hozir sotuvda bo\'lgan barcha mahsulotlar:', reply_markup=markup)
    
async def meat(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🔹 Mol go`shti')
    button2 = types.KeyboardButton('🔹 Tovuq go`shti')
    button3 = types.KeyboardButton('🔹 Qo`y go`shti')
    button4 = types.KeyboardButton('🔹 Qiyma go`sh')
    button5 = types.KeyboardButton('🗓 Kategoriya')
    markup.row(button5)
    markup.row(button1, button2)
    markup.row(button3, button4)
    await bot.send_message(message.chat.id, 'Hozir sotuvda bo\'lgan barcha mahsulotlar:', reply_markup=markup)
    
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
    await bot.send_message(message.chat.id, 'Hozir sotuvda bo\'lgan barcha mahsulotlar:', reply_markup=markup)



async def settingsChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("🌐 Tilni o'zgartirish")
    button3 = types.KeyboardButton('↩️ Menyuga qaytish')
    markup.row(button1, button3)
    await bot.send_message(message.chat.id, 'Sozlamalar bo\'limi.\nBir variantni tanlang:', reply_markup=markup)

async def infoChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('✏️ Dasturchiga yozish')
    button2 = types.KeyboardButton('↩️ Menyuga qaytish')
    button3 = types.KeyboardButton("📄 Ma'lumotnoma")
    markup.row(button1, button3)
    markup.row(button2)
    await bot.send_message(message.chat.id, 'Yordam bo\'limi.\nBu erda siz dasturchiga xabar yozishingiz mumkin.', reply_markup=markup)

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
    button1 = types.KeyboardButton("🚚 Buyurtma berish")
    button2 = types.KeyboardButton("↩️ Orqaga qaytish")
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
