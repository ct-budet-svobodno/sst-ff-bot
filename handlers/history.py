from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from keyboards.inline import return_to_start
from content.text_content import history as hc

history_router = Router()
content = hc

@history_router.callback_query(F.data == "history_pressed")
async def history_report(call:CallbackQuery):
    await call.message.answer(text=content, parse_mode=ParseMode.HTML, reply_markup=return_to_start())
    await call.answer()