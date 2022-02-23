from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.types import CallbackQuery

from data.config import ADMINS
from keyboards.default import menu, okno
from keyboards.inline.manage_post import post_callback, confirmation_keyboard
from loader import dp, bot
from states import Ishjoy
from states.newpost import NewPost


@dp.message_handler(state=Ishjoy.idora)
async def photo_handler(msg: types.Message, state: FSMContext):
    idora = msg.text
    await state.update_data(
        {"idora": idora}
    )
    await msg.answer("""📚 Texnologiya:

Talab qilinadigan texnologiyalarni kiriting?
Texnologiya nomlarini vergul bilan ajrating. Masalan, 

Java, C++, C#""")
    await Ishjoy.tecnology.set()


@dp.message_handler(state=Ishjoy.tecnology)
async def photo_handler(msg: types.Message, state: FSMContext):
    tec = msg.text
    await state.update_data(
        {"tecnology": tec}
    )
    await msg.answer("""📞 Aloqa: 

Bog`lanish uchun raqamingizni kiriting?
Masalan, +998 90 123 45 67""")
    await Ishjoy.tel.set()


@dp.message_handler(state=Ishjoy.tel)
async def photo_handler(msg: types.Message, state: FSMContext):
    tel = msg.text
    await state.update_data(
        {"number": tel}
    )
    await msg.answer("""🌐 Hudud: 

Qaysi hududdansiz?
Viloyat nomi, Toshkent shahar yoki Respublikani kiriting.""")
    await Ishjoy.hudud.set()


@dp.message_handler(state=Ishjoy.hudud)
async def photo_handler(msg: types.Message, state: FSMContext):
    hudud = msg.text
    await state.update_data(
        {"hudud": hudud}
    )
    await msg.answer("""✍️Mas'ul ism sharifi?""")
    await Ishjoy.ism_fam.set()


@dp.message_handler(state=Ishjoy.ism_fam)
async def photo_handler(msg: types.Message, state: FSMContext):
    ism_fam = msg.text
    await state.update_data(
        {"name": ism_fam}
    )
    await msg.answer("""🕰 Murojaat qilish vaqti: 

Qaysi vaqtda murojaat qilish mumkin?
Masalan, 9:00 - 18:00""")
    await Ishjoy.time.set()


@dp.message_handler(state=Ishjoy.time)
async def photo_handler(msg: types.Message, state: FSMContext):
    time = msg.text
    await state.update_data(
        {"time": time}
    )
    await msg.answer("""🕰 Ish vaqtini kiriting?""")
    await Ishjoy.maosh.set()


@dp.message_handler(state=Ishjoy.ish_vaqti)
async def photo_handler(msg: types.Message, state: FSMContext):
    work_time = msg.text
    await state.update_data(
        {"work_time": work_time}
    )
    await msg.answer("""💰 Maoshni kiriting?""")
    await Ishjoy.maosh.set()


@dp.message_handler(state=Ishjoy.maosh)
async def photo_handler(msg: types.Message, state: FSMContext):
    earn = msg.text
    await state.update_data(
        {"maosh": earn}
    )
    await msg.answer("""‼️ Qo`shimcha ma`lumotlar?""")
    await Ishjoy.qoshimcha.set()


@dp.message_handler(state=Ishjoy.qoshimcha)
async def photo_handler(msg: types.Message, state: FSMContext):
    qoshimcha = msg.text
    await state.update_data(
        {"qoshimcha": qoshimcha}
    )


    data = await state.get_data()

    idora = data.get("idora")
    tecnology = data.get("tecnology")
    phone_num = data.get("number")
    hudud = data.get("hudud")
    name = data.get("name")
    time = data.get("time")
    work_time = data.get("work_time")
    maosh = data.get("maosh")
    qoshimcha = data.get("qoshimcha")

    post = f"""Xodim kerak:

🏢 Idora: {idora}
📚 Texnologiya: {tecnology} 
📞 Aloqa: {phone_num} 
🌐 Hudud: {hudud}
✍️ Mas'ul: {name}
🕰 Murojaat vaqti: {time} 
🕰 Ish vaqti: {work_time} 
💰 Maosh: {maosh}
‼️ Qo`shimcha: {qoshimcha}

E'lon berish uchun:
🤖@UteamWorkbot

#ishJoyi
"""
    message = await msg.answer(post)
    await msg.answer("Barcha ma'lumotlar to'g'rimi?", reply_markup=okno)
    await state.update_data(text=message.html_text, mention=msg.from_user.get_mention(), user_id=msg.from_user.id,
                            id=msg.from_user.id)
    await NewPost.NewMessage.set()


@dp.message_handler(text="Yo'q", state="*")
async def jdpoq(msg: types.Message, state: FSMContext):
    if state:
        await state.finish()
    await msg.answer("Muvaffaqiyatli bekor qilindi ✅ ", reply_markup=menu)


@dp.message_handler(text='Ha', state=NewPost.NewMessage)
async def jdpoq(msg: types.Message, state: FSMContext):
    await msg.answer("Ma'lumotlar to'griligini tasdiqladingiz", reply_markup=menu)
    await msg.answer("Chop etish tugmasini bossangiz postni tekshirish "
                     "uchun yuboriladi.", reply_markup=confirmation_keyboard)
    await NewPost.next()


@dp.callback_query_handler(post_callback.filter(action="post"), state=NewPost.Confirm)
async def confirm_post(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        text = data.get("text")
        mention = data.get('mention')
        user_id = data.get('user_id')
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Post adminga yuborildi")
    await bot.send_message(ADMINS[0], f"Foydalanuvchi {mention} id = {user_id} quyidagi postni chop etmoqchi: ")
    await bot.send_message(ADMINS[0], text, parse_mode="HTML", reply_markup=confirmation_keyboard)


@dp.callback_query_handler(post_callback.filter(action="cancel"), state=NewPost.Confirm)
async def cancel_post(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Post rad etildi")


@dp.message_handler(state=NewPost.Confirm)
async def post_unknown(message, Message):
    await message.answer("Chop etish yoki rad etishni tanlang")


@dp.callback_query_handler(post_callback.filter(action="post"), user_id=ADMINS)
async def approve_post(call: CallbackQuery, state: FSMContext):
    await call.answer(f"Chop etishga ruxsat berdingiz .", show_alert=True)
    target_channel = "@UteamWorkuz"
    message = await call.message.edit_reply_markup()
    await message.send_copy(chat_id=target_channel)
    # await bot.send_message(chat_id=user_id, text="So'rovingiz muvaffaqiyatli yakunlandi . @UteamWorkuz kanaliga joylandi.")


@dp.callback_query_handler(post_callback.filter(action='cancel'), user_id=ADMINS)
async def decline_post(call: CallbackQuery, state: FSMContext):
    await call.answer("Post rad etildi. ", show_alert=True)
    await call.message.edit_reply_markup()
    # await bot.send_message(chat_id=user_id, text="So'rovingiz muvaffaqiyatsiz yakunlandi.")

