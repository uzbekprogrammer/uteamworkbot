import pysqlite3

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from keyboards.default import menu
from loader import dp, db, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    user_id = message.from_user.id
    # Foydalanuvchini bazaga qoshamiz
    try:
        db.add_user(id=message.from_user.id,
                    name=name)
        count = db.count_users()[0]
        msg = f'<a href="tg://user?id={user_id}">{name}</a> bazaga qoshildi. \nBazada {count} ta foydalanuvchi bor.' \
              f'\nID {user_id}.'
        await bot.send_message(chat_id=ADMINS[0], text=msg)

    except pysqlite3.IntegrityError as err:
        # await bot.send_message(chat_id=ADMINS[0], text=err)
        pass
    await message.answer(f"""Assalom alaykum {message.from_user.full_name}!
@UteamWorkuz kanalining rasmiy botiga xush kelibsiz!
Quyidagi menulardan birini bosing.

/help yordam buyrugi orqali nimalarga qodir ekanligimni bilib oling!""", reply_markup=menu)


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    if state:
        await state.finish()
    await message.answer(f"Salom, {message.from_user.full_name}!\nSizni ko'ganimizdan hursandmiz", reply_markup=menu)
