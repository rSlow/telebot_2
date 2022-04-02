from string import punctuation
from bot import dispatcher, bot
from cenz import cenz
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from keyboards import get_main_keyboard


@dispatcher.message_handler(Text(equals="↪ На главную"), state="*")
async def to_main_menu(message: types.Message, state: FSMContext):
    user_data = message.from_user
    users = bot.users
    if user_data.id not in users:
        users.append(user_data.id)
        print(f"[NEW USER] {user_data.username}:{user_data.id}")

    if await state.get_state():
        await state.finish()
    await message.answer("Возвращаем в главное меню...",
                         reply_markup=get_main_keyboard(message.from_user.id))


@dispatcher.message_handler(commands=['cancel'], state="*")
async def cancel(message: types.Message, state: FSMContext):
    if await state.get_state():
        await state.finish()
    await message.answer("Отменено.",
                         reply_markup=get_main_keyboard(message.from_user.id))


@dispatcher.message_handler(state="*")
async def censorship(message: types.Message):
    if message.from_user.id != message.chat.id:
        if {word.lower().translate(str.maketrans("", "", punctuation)) for word in message.text.split()} & cenz:
            await message.reply(f"{message.from_user.mention} не матерись!")
            await message.delete()
    else:
        await message.delete()
