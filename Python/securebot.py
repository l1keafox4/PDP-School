import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from aiogram.types import Message, ParseMode


API_TOKEN = '6905287917:AAFSBi33u53XOf1VSVGBFdwzT5mQQGNdw0s'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

stats = {}

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.reply("Привет! Я бот, который может банить, мутить и кикать пользователей. "
                        "Просто добавь меня в группу и дай админские права!")


@dp.message_handler(commands=['tempkick'])
async def tempkick_user(message: types.Message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = await bot.get_chat_member(chat_id, user_id)

        if user_status.is_chat_admin():
            await message.reply("Невозможно кикнуть администратора.")
        else:
            try:
                duration = int(message.text.split()[1])
                await bot.kick_chat_member(chat_id, user_id)
                await message.reply(f"Пользователь {message.reply_to_message.from_user.username} был кикнут на {duration} секунд.")

                await asyncio.sleep(duration)  # Ожидаем время блокировки

                await bot.unban_chat_member(chat_id, user_id)
                await message.reply(f"Пользователь {message.reply_to_message.from_user.username} был разблокирован.")
            except (IndexError, ValueError):
                await message.reply("Пожалуйста, укажите время в секундах после команды /tempkick.")
    else:
        await message.reply("Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите кикнуть.")

@dp.message_handler(commands=['kick'])
async def kick_user(message: types.Message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        await bot.kick_chat_member(chat_id, user_id)
        await message.reply(f"Пользователь {message.reply_to_message.from_user.username} был кикнут.")
    else:
        await message.reply("Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите кикнуть.")


@dp.message_handler(commands=['unkick'])
async def unkick_user(message: types.Message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        await bot.unban_chat_member(chat_id, user_id)
        await message.reply(f"Пользователь {message.reply_to_message.from_user.username} разблокирован.")
    else:
        await message.reply("Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите разблокировать после кика.")



@dp.message_handler(commands=['tempban'])
async def tempban_user(message: types.Message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = await bot.get_chat_member(chat_id, user_id)

        # if user_status.is_chat_admin():
        #     await message.reply("Невозможно забанить администратора.")
        if user_status.is_chat_owner():
            await message.reply("Невозможно забанить администратора.")
        elif user_status.is_chat_admin():
            try:
                duration = int(message.text.split()[1])
                await bot.ban_chat_member(chat_id, user_id)
                await message.reply(f"Пользователь {message.reply_to_message.from_user.username} был забанен на {duration} секунд.")

                await asyncio.sleep(duration)

                await bot.unban_chat_sender_chat(chat_id, user_id)
                await message.reply(f"Пользователь {message.reply_to_message.from_user.username} был разбанен.")
            except (IndexError, ValueError):
                await message.reply("Пожалуйста, укажите время в секундах после команды /tempban.")
        else:
            try:
                duration = int(message.text.split()[1])
                await bot.ban_chat_member(chat_id, user_id)
                await message.reply(f"Пользователь {message.reply_to_message.from_user.username} был забанен на {duration} секунд.")

                await asyncio.sleep(duration)

                await bot.unban_chat_member(chat_id, user_id)
                await message.reply(f"Пользователь {message.reply_to_message.from_user.username} был разбанен.")
            except (IndexError, ValueError):
                await message.reply("Пожалуйста, укажите время в секундах после команды /tempban.")
    else:
        await message.reply("Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")

@dp.message_handler(commands=['ban'])
async def ban_user(message: types.Message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        await bot.ban_chat_member(chat_id, user_id)
        await message.reply(f"Пользователь {message.reply_to_message.from_user.username} был забанен.")
    else:
        await message.reply("Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")


@dp.message_handler(commands=['unban'])
async def unban_user(message: types.Message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        await bot.unban_chat_member(chat_id, user_id)
    else:
        await message.reply("Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите разбанить.")



@dp.message_handler(commands=['tempmute'])
async def tempmute_user(message: types.Message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = await bot.get_chat_member(chat_id, user_id)

        # if user_status.is_chat_owner():
        #     await message.reply("Невозможно замутить администратора.")
        if user_status.is_chat_admin():
            await message.reply("Невозможно замутить администратора.")
        else:
            try:
                permissions = types.ChatPermissions()
                permissions.send_messages = False
                permissions.send_media_messages = False
                permissions.send_polls = False
                permissions.change_info = False
                permissions.add_admins = False
                permissions.pin_messages = False

                duration = int(message.text.split()[1])
                await bot.restrict_chat_member(chat_id, user_id, permissions)
                await message.reply(f"Пользователь {message.reply_to_message.from_user.username} был замучен на {duration} секунд.")

                await asyncio.sleep(duration)  # Ожидаем время блокировки

                await untempmute_user(message)

                await message.reply(f"Пользователь {message.reply_to_message.from_user.username} был размучен.")
            except (IndexError, ValueError):
                await message.reply("Пожалуйста, укажите время в секундах после команды /tempmute.")
    else:
        await message.reply("Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите замутить.")

@dp.message_handler(commands=['untempmute'])
async def untempmute_user(message: types.Message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        permissions = types.ChatPermissions()
        permissions.send_messages = True
        permissions.send_media_messages = True
        permissions.send_polls = True
        permissions.change_info = True
        permissions.add_admins = True
        permissions.pin_messages = True
        await bot.restrict_chat_member(chat_id, user_id, permissions)


@dp.message_handler(commands=['mute'])
async def mute_user(message: types.Message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        await bot.restrict_chat_member(chat_id, user_id)
        await message.reply(f"Пользователь {message.reply_to_message.from_user.username} был замучен.")
    else:
        await message.reply("Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите замутить.")

@dp.message_handler(commands=['unmute'])
async def unmute_user(message: types.Message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        await bot.restrict_chat_member(chat_id, user_id)
        await message.reply(f"Пользователь {message.reply_to_message.from_user.username} был размучен.")
    else:
        await message.reply("Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите размутить.")



@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply("Доступные команды:\n"
                        "/ban - забанить пользователя\n"
                        "/unban - разбанить пользователя\n"
                        "/kick - кикнуть пользователя\n"
                        "/mute - замутить пользователя\n"
                        "/unmute - размутить пользователя\n"
                        "/tempban - банить пользователя на определенное время\n"
                        "/tempmute - мутить пользователя на определенное время\n"
                        "/unkick - разбанить пользователя после кика\n"
                        "/help - помощь по командам\n"
                        "/selfstat - статистика группи\n")


@dp.message_handler(commands=['stats'])
async def chat_stats(message: types.Message):
    chat_id = message.chat.id
    if chat_id not in stats:
        await message.reply("Статистика чата пуста.")
    else:
        total_messages = stats[chat_id]['total_messages']
        unique_users = len(stats[chat_id]['users'])
        await message.reply(f"Статистика чата:\nВсего сообщений: {total_messages}\nУникальных пользователей: {unique_users}")

@dp.message_handler(commands=['selfstat'])
async def user_stats(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    if chat_id not in stats:
        await message.reply("Статистика чата пуста.")
    else:
        if user_id not in stats[chat_id]['users']:
            await message.reply("Вы еще не отправляли сообщений в этом чате.")
        else:
            user_messages = stats[chat_id]['users'][user_id]['messages']
            total_messages = stats[chat_id]['total_messages']
            percentage = round(user_messages / total_messages * 100, 2)
            await message.reply(f"Статистика для пользователя @{username}:\nВсего сообщений: {user_messages}\nПроцент от общего количества сообщений: {percentage}%", parse_mode=ParseMode.HTML)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
