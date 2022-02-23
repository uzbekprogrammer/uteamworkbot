from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, user

from data.config import ADMINS, CHANNELS
from keyboards.default import okno, menu
from keyboards.inline import confirmation_keyboard
from keyboards.inline.manage_post import post_callback
from loader import dp, bot
from states import Ishchi
from states.newpost import NewPost


@dp.message_handler(state=Ishchi.ism_fam)
async def photo_handler(msg: types.Message, state: FSMContext):
    fullname = msg.text
    await state.update_data(
        {"name": fullname}
    )
    await msg.answer("""🕑 Yosh: 

Yoshingizni kiriting?
Masalan, 17""")
    await Ishchi.yosh.set()


@dp.message_handler(state=Ishchi.yosh)
async def photo_handler(msg: types.Message, state: FSMContext):
    age = msg.text
    await state.update_data(
        {"age": age}
    )
    await msg.answer("""📚 Texnologiya:

Talab qilinadigan texnologiyalarni kiriting?
Texnologiya nomlarini vergul bilan ajrating. Masalan, 

Java, Python, React, Django""")
    await Ishchi.texnology.set()


@dp.message_handler(state=Ishchi.texnology)
async def asdasd(msg: types.Message, state: FSMContext):
    tec = msg.text
    await state.update_data(
        {'tecnology': tec}
    )

    await msg.answer("""📞 Aloqa: 

Bog`lanish uchun raqamingizni kiriting?
Masalan, +998901234567""")
    await Ishchi.tel.set()


@dp.message_handler(state=Ishchi.tel)
async def asdasd(msg: types.Message, state: FSMContext):
    number = msg.text
    await state.update_data(
        {'num': number}
    )

    await msg.answer("""🌐 Hudud: 

Qaysi hududdansiz?
Viloyat nomi, Toshkent shahar yoki Respublikani kiriting.""")
    await Ishchi.hudud.set()


@dp.message_handler(state=Ishchi.hudud)
async def asdasd(msg: types.Message, state: FSMContext):
    hudud = msg.text
    await state.update_data(
        {'hudud': hudud}
    )

    await msg.answer("""💰 Narxi:

Qancha maosh hohlaysiz?""")
    await Ishchi.narx.set()


@dp.message_handler(state=Ishchi.narx)
async def asdasd(msg: types.Message, state: FSMContext):
    narx = msg.text
    await state.update_data(
        {'narx': narx}
    )
    await msg.answer("""👨🏻‍💻 Kasbi: 

Ishlaysizmi yoki o`qiysizmi?
Masalan, Talaba""")
    await Ishchi.kasb.set()


@dp.message_handler(state=Ishchi.kasb)
async def asdasd(msg: types.Message, state: FSMContext):
    kasb = msg.text
    await state.update_data(
        {'kasb': kasb}
    )
    await msg.answer("""🕰 Murojaat qilish vaqti: 

Qaysi vaqtda murojaat qilish mumkin?
Masalan, 9:00 - 18:00""")
    await Ishchi.time.set()


@dp.message_handler(state=Ishchi.time)
async def asdasd(msg: types.Message, state: FSMContext):
    time = msg.text
    await state.update_data(
        {'time': time}
    )
    await msg.answer("""🔎 Maqsad: 

Maqsadingizni qisqacha yozib bering.""")
    await Ishchi.maqsad.set()


@dp.message_handler(state=Ishchi.maqsad)
async def asdasd(msg: types.Message, state: FSMContext):
    maqsad = msg.text
    await state.update_data(
        {'maqsad': maqsad}
    )

    data = await state.get_data()

    fullname = data.get("name")
    age = data.get("age")
    tecnology = data.get("tecnology")
    num = data.get("num")
    hudud = data.get("hudud")
    narx = data.get("narx")
    kasb = data.get("kasb")
    time = data.get("time")
    maqsad = data.get("maqsad")

    post = f"""Ish joyi kerak:

👨‍💼 Xodim: {fullname}
🕑 Yosh: {age}
📚 Texnologiya: {tecnology} 
📞 Aloqa: {num} 
🌐 Hudud: {hudud} 
💰 Narxi: {narx} 
👨🏻‍💻 Kasbi: {kasb} 
🕰 Murojaat qilish vaqti: {time} 
🔎 Maqsad: {maqsad} 

E'lon berish uchun:
🤖@UteamWorkbot

#xodim"""
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

