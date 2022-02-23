from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

okno = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ha"),
            KeyboardButton(text="Yo'q")
        ],
    ],
    resize_keyboard=True
)
