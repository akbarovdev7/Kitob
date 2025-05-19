import json

import asyncio
import html
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
TOKEN = "8074931699:AAECp_95TvWhcueriLFR7xItgBmUjY8ltac"
ADMIN_ID = 7176798576



PDF_DB_FILE = "kitob.json"


bot = Bot(token=TOKEN,default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
CHANNELS = [
    {
        "link": "https://t.me/kfkhfvx",  # Kanal havolasi
        "username": "@kfkhfvx"       # Kanal USERNAME'si (e.g., @ustozIT)
    }
]
async def check_subscription(user_id: int) -> bool:
    for channel in CHANNELS:
        chat_member = await bot.get_chat_member(chat_id=channel["id"], user_id=user_id)
        if chat_member.status not in ["member", "administrator", "creator"]:
            return False
    return True
TEXT_WELCOME1 = (
    "<b>Assalomu alaykum👋🏻! \n"
    "PDF kitoblar qidiruv botiga xush kelibsiz📚\n\n"
    "Istagan kitob nomini yuboring. <i>Masalan:</i> <code>Qora Psixologiya</code>\n"
    "Biz siz uchun kerakli kitobni topishga harakat qilamiz. 🔍\n\n"
    "Qidiruvni boshlash uchun shunchaki kitob nomini yozing✍️</b>"
)



TEXT_WELCOME = (
    "<b>Assalomu alaykum👋🏻! \n"
    "PDF kitoblar qidiruv botiga xush kelibsiz📚\n\n"
    "Istagan kitob nomini yuboring. <i>Masalan:</i> <code>Qora Psixologiya</code>\n"
    "Biz siz uchun kerakli kitobni topishga harakat qilamiz. 🔍\n\n"
    "Qidiruvni boshlash uchun shunchaki kitob nomini yozing✍️</b>"
)


TEXT_NEED_SUBSCRIBE = "❌ Botdan foydalanish uchun quyidagi kanalga a'zo bo'ling:"

# 📌 /start komandasi
@dp.message(Command("start"))
async def start_command(message: types.Message):
    user_id = message.from_user.id

    if await check_subscription(user_id):
        await message.answer(TEXT_WELCOME1)
    else:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📢 Obuna bo'lish", url=CHANNELS[0]["link"])],
                [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subscription")]
            ]
        )
        await message.answer(TEXT_NEED_SUBSCRIBE, reply_markup=markup)

# 📌 Obunani tekshirish tugmasi
@dp.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if await check_subscription(user_id):
        await callback.message.edit_text(TEXT_WELCOME)
    else:
        await callback.answer("❌ Iltimos, avval kanalga obuna bo'ling!", show_alert=True)

# 📌 Obunani tekshirish funksiyasi (faqat bitta kanal uchun)
async def check_subscription(user_id):
    channel_username = CHANNELS[0]["username"]  # masalan: "@yourchannel"
    try:
        member = await bot.get_chat_member(chat_id=channel_username, user_id=user_id)
        return member.status in ["member", "creator", "administrator"]
    except:
        return False
def load_files():
    try:
        with open(PDF_DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_files(data):
    with open(PDF_DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

files = load_files()

# Handlerlarni ro'yxatdan o'tkazish uchun funktsiya
@dp.message(lambda message: message.from_user.id == ADMIN_ID and message.document and message.document.mime_type == "application/pdf")
async def save_pdf(message: Message):
    file_id = message.document.file_id
    caption = message.caption or f"pdf_{len(files)+1}"

    files[caption] = file_id
    save_files(files)

    await message.answer(f"✅ PDF saqlandi: `{caption}`")

@dp.message(Command("files"))
async def list_files(message: Message):
    if not files:
        await message.answer("❌ Hozircha hech qanday PDF saqlanmagan.")
        return

    text = "📂 Saqlangan PDF fayllar:\n" + "\n".join(f"- {name}" for name in files.keys())
    await message.answer(text)

@dp.message()
async def send_saved_pdf(message: Message):
    file_id = files.get(message.text)
    if file_id:
        await bot.send_document(chat_id=message.chat.id, document=file_id, caption=f"📄 {message.text}")
    else:
        await message.answer("❌ Pdf kitob topilmadi. Kitob nomi to'g'riligini tekshiring.")

if __name__ == "__main__":
    print("Bot ishga tushdi...")
    import asyncio
    asyncio.run(dp.start_polling(bot))
