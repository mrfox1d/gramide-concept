from aiogram.filters import Command
from aiogram import types, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from databases.dbs import Database

router = Router()
db = Database("database.db")

@router.message(Command(commands=['start']))
async def cmd_start(message: types.Message):
    user = await db.get_user(message.from_user.id)
    
    if not user:
        mk = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🇷🇺 Русский",
                    callback_data="ru"
                ),
                InlineKeyboardButton(
                    text="🇺🇸 English",
                    callback_data="en"
                )
            ]
        ])
        await message.answer("🇷🇺 **Выберите ваш язык:**\n🇺🇸 **Choose your language:**", reply_markup=mk, parse_mode="Markdown")
    else:
        if user[1] == "ru":
            await message.answer(f"С возвращением, {message.from_user.first_name}!")
        elif user[1] == "en":
            await message.answer(f"Welcome back, {message.from_user.first_name}!")

@router.callback_query(lambda c: c.data in ["ru", "en"])
async def set_language(callback: types.CallbackQuery):
    await db.add_user(callback.from_user.id, callback.data)
    
    if callback.message:
        if callback.data == "ru":
            await callback.message.edit_text("🇷🇺 Язык установлен на русский.")
            await callback.message.answer(
                f"👋 Приветствую тебя, {callback.message.from_user.first_name}!\n\nЯ - Бордли, бот с настолками в Telegram. Нажми кнопку ниже, чтобы начать играть!",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="🎲 Играть",
                            web_app=WebAppInfo(url="https://brdly.space")
                        )
                    ]
                ])
                )
            
        elif callback.data == "en":
            await callback.message.edit_text("🇺🇸 Language set to English.")
            await callback.message.answer(
                f"👋 Glad to see you, {callback.message.from_user.first_name}!\n\nI'm Bordly, a board game bot in Telegram. Click the button below to start playing!",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="🎲 Play",
                            web_app=WebAppInfo(url="https://brdly.space")
                        )
                    ]
                ])
            )