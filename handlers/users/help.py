from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp(), state="*")
async def bot_help(message: types.Message, state=FSMContext):
    if state:
        await state.finish()
    text = ("Bu yerda <b>Dasturlash</b> bo'yicha xodim va ish joyi boyicha e'lon berishingiz mumkin")
    
    await message.answer(text)
