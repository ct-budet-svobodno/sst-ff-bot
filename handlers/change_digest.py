import os
from pathlib import Path
from aiogram import Router, F, types, Bot
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
# from sqlalchemy.ext.asyncio import AsyncSession
from config import BOT_TOKEN
from keyboards.inline import return_to_start, assurance
from database.crud import delete_activist
from database.engine import get_session

change_digest_router = Router()
bot = Bot(token=BOT_TOKEN)
UPLOAD_DIR = Path(__file__).resolve().parent.parent / "content"

class Change_digest(StatesGroup):
    month = State()
    photo = State()

@change_digest_router.callback_query(F.data == "change_digest_pressed")
async def add_text(call:CallbackQuery, state:FSMContext):
    await call.message.answer('🌸 Введите текст, сопровождающий дайджест.\nПример: "Дайджест на сентябрь".')
    await call.answer()
    await state.set_state(Change_digest.month)

@change_digest_router.message(Change_digest.month, F.text)
async def assurance_clarify(message:types.Message, state:FSMContext):
    await state.update_data(month=message.text)
    await message.answer('Сохранено! 🌸\nТеперь отправьте дайджест в формате JPEG размером до 1 МБ: ')
    await state.set_state(Change_digest.photo)

@change_digest_router.message(Change_digest.photo, F.photo)
async def add_birthday(message:types.Message, state:FSMContext):
    await state.update_data(photo=message.photo[-1])
    await message.answer('Сохранено!...')
    content = await state.get_data()
    month = content.get('month')
    photo = content.get('photo')
    file_info = await bot.get_file(photo.file_id)
    destination = os.path.join(UPLOAD_DIR, 'digest.jpg')
    await bot.download(file_info, destination=destination)
    print(f'!!!Фото сохранилось в {destination}')
    with open('content/digest_content.txt', 'w', encoding='utf-8') as f:
        f.write(month)
    await message.answer("Дайджест загружен!✅", reply_markup=return_to_start())