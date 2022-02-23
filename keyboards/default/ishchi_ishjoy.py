#  Created by Abdurahim Mahmudov
#  Namangan, Uzbekistan

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ish joyi kerak"),
            KeyboardButton(text="Hodim kerak")
        ],
    ],
    resize_keyboard=True
)