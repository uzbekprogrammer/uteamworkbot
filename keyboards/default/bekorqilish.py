
#  Created by Abdurahim Mahmudov
#  Namangan, Uzbekistan

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

out = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❌Bekor qilish"),
        ],
    ],
    resize_keyboard=True
)