
import json
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import asyncio
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Загружаем контент
with open("content.json", encoding="utf-8") as f:
    content = json.load(f)["lessons"]

# Хендлер на /start
@dp.message(F.text == "/start")
async def start_handler(message: Message):
    kb = ReplyKeyboardBuilder()
    for i in range(1, 11):
        kb.button(text=f"Урок {i}")
    await message.answer("Привет! Я — Шелли. Выбери, на каком уроке ты сейчас:", reply_markup=kb.as_markup(resize_keyboard=True))

# Выбор урока
@dp.message(F.text.regexp(r"Урок \d+"))
async def lesson_handler(message: Message):
    lesson_number = message.text.split()[1]
    lesson = content.get(lesson_number)
    if not lesson:
        await message.answer("Этот урок пока не добавлен.")
        return
    kb = ReplyKeyboardBuilder()
    for subsection in lesson["subsections"]:
        kb.button(text=f"{lesson_number}.{subsection}")
    await message.answer(f"{lesson['title']}. Выбери раздел:", reply_markup=kb.as_markup(resize_keyboard=True))

# Выбор подраздела
@dp.message(F.text.regexp(r"\d+\.\d+"))
async def subsection_handler(message: Message):
    key = message.text.strip()
    lesson_num, subsec_num = key.split(".")
    lesson = content.get(lesson_num)
    if not lesson or subsec_num not in lesson["subsections"]:
        await message.answer("Этот раздел пока не добавлен.")
        return
    subsection = lesson["subsections"][subsec_num]
    text = f"<b>{subsection['title']}</b>\n\n"
    for item in subsection["qa"]:
        text += f"❓ <b>{item['q']}</b>\n{item['a']}\n\n"
    await message.answer(text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
