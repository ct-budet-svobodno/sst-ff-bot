import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database.engine import create_db, import_users, is_table_empty
from handlers.start import start_router
from handlers.history import history_router
from handlers.pvr import pvr_router
from handlers.tutor_tree import tutr_router
from handlers.friends import friends_router
from handlers.ach_kos import ak_router
from handlers.my_raiting import raiting_router
from handlers.digest import digest_router 
from handlers.contacts import contact_router
from handlers.admin_rights import admin_router
from handlers.show_ak import show_ak_router
from handlers.search import search_router


logging.basicConfig(level=logging.INFO)

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN)
dp.include_router(start_router)
dp.include_router(history_router)
dp.include_router(pvr_router)
dp.include_router(tutr_router)
dp.include_router(friends_router)
dp.include_router(ak_router)
dp.include_router(raiting_router)
dp.include_router(digest_router)
dp.include_router(contact_router)
dp.include_router(admin_router)
dp.include_router(show_ak_router)
dp.include_router(search_router)

async def main():
    await create_db()
    count = await is_table_empty()
    if count == 0:
        print(f'БД: {count}')
        await import_users()
    await dp.start_polling(bot)
    print("Бот запущен")

if __name__ == '__main__':
    asyncio.run(main())