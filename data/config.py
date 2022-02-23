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

BOT_TOKEN = str(os.environs.str("BOT_TOKEN"))  # Bot toekn
ADMINS = list(os.environs.list("ADMINS"))  # adminlar ro'yxati
IP = str(os.environs.str("ip"))  # Xosting ip manzili
CHANNELS = str(os.environs.str("CHANNEL"))
PROVIDER_TOKEN = str(os.environs.str("PROVIDER_TOKEN"))
