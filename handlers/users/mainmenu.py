from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import menu, out
from loader import dp
from states import Ishchi, Ishjoy


@dp.message_handler(text="Ish joyi kerak")
async def ishchi(message: types.Message):
    await Ishchi.ism_fam.set()
    await message.reply("""Ish joyi topish uchun ariza berish

Hozir sizga birnecha savollar beriladi. 
Har biriga javob bering. 
Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.""", reply_markup=out)
    await message.reply("Ism familiyangizni kiriting")


@dp.message_handler(text="Hodim kerak")
async def forishjoy(message: types.Message):
    await Ishjoy.idora.set()

    await message.reply("""Xodim topish uchun ariza berish

Hozir sizga birnecha savollar beriladi. 
Har biriga javob bering. 
Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.""", reply_markup=out)
    await message.answer(text='🎓 Idora nomi?')


@dp.message_handler(text="❌Bekor qilish", state="*")
async def bekor(message: types.Message, state: FSMContext):
    if state:
        await state.finish()
    await message.answer("Muvaffaqiyatli bekor qilindi ✅ ", reply_markup=menu)
