from aiogram import Bot, Dispatcher
import asyncio
import os
from dotenv import load_dotenv
from databases.dbs import Database
from handlers import start

db = Database("database.db")

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    print("⚙️ Инициализация базы данных...")
    await db.init_db()
    print("✅ База данных готова!")

    dp.include_router(start.router)
    print("✅ Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())