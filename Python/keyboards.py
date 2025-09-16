from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
text = "1"

summa_edit = 0
amount_edit = 0
user = 0
find = 0
find_manager = 0
info_ok = 0
usernam = ''
delivery_info = ''
delivery = 0
order_ok = 0
lang = ''
korzinka = {}
korzinka = {}

current_value = 0
keyboardss = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("+", callback_data='plus'),InlineKeyboardButton(f"{current_value}", callback_data="amount"),InlineKeyboardButton("-", callback_data='minus')],
            [InlineKeyboardButton("Добавить в корзину", callback_data='add_cart')]
    ])
keyboard_manager = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("Изменить стоимость", callback_data='edit_summa')],
            [InlineKeyboardButton("Изменить наличие", callback_data='edit_amount')]])
async def button_exe() -> InlineKeyboardMarkup:
    global current_value
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(f"{current_value}", callback_data="update_button"))
    return markup