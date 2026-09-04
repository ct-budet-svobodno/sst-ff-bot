from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from keyboards.inline import return_to_start

tutr_router = Router()

@tutr_router.callback_query(F.data == "tutr_pressed")
async def tutr_report(call:CallbackQuery):
    await call.message.answer("🌳 <u>Тьюторское дерево</u>\n\n<a href='https://drive.google.com/file/d/1HuAkGOwji_yVrXpq2RA3QMXNDIzBcpod/view?usp=sharing'>ССЫЛКА</a>",
                                request_timeout=300,
                                reply_markup=return_to_start(),
                                parse_mode=ParseMode.HTML)
    await call.answer()