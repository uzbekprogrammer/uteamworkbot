# from environs import Env
#
# # environs kutubxonasidan foydalanish
# env = Env()
# env.read_env()
#
# # .env fayl ichidan quyidagilarni o'qiymiz
# BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
# ADMINS = env.list("ADMINS")  # adminlar ro'yxati
# IP = env.str("ip")  # Xosting ip manzili
# CHANNELS = env.str("CHANNEL")

import os

BOT_TOKEN = str(os.environ.str("BOT_TOKEN"))  # Bot toekn
ADMINS = list(os.environ.list("ADMINS"))  # adminlar ro'yxati
IP = str(os.environ.str("ip"))  # Xosting ip manzili
CHANNELS = str(os.environ.str("CHANNEL"))
