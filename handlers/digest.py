import os
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.enums import ParseMode
from keyboards.inline import return_to_start

digest_router = Router()

@digest_router.callback_query(F.data == "digest_pressed")
async def digest_report(call:CallbackQuery):
    photo = FSInputFile("content/digest.jpg")
    file_path = "content/digest_content.txt"
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            digest_text = f.read()
    else:
        print("!!!Файл текста дайджеста не найден")
    await call.message.answer_photo(photo,
                                caption=f'📆 {digest_text}',
                                request_timeout=300,
                                reply_markup=return_to_start(),
                                parse_mode=ParseMode.HTML)
    await call.answer()