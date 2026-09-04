from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from keyboards.inline import return_to_start
from database.engine import get_session
from database.crud import get_rate

raiting_router = Router()

def generate_report(name, score, ach_kos, status):
    if ach_kos == None:
        ach_kos =  "🫥 Пока не получено"
    report = (
            f"🦊<u><b>{name}</b></u>\n"
            f"├ Статус: {status}\n"
            f"├ Баллы: <b>{score}</b>\n"
            f"└ Последние ачивки и косяки:\n{ach_kos}"
    )
    return report

@raiting_router.callback_query(F.data == "raiting_pressed")
async def rate_report(call:CallbackQuery):
    async for session in get_session():
        telegram_id = call.from_user.username if call.from_user.username[0]=='@' else '@' + call.from_user.username
        user = await get_rate(session, telegram_id)
        if user is not None:
            report = generate_report(user.name, user.score, user.ach_kos, user.status)
            await call.message.answer(report, reply_markup=return_to_start(), parse_mode=ParseMode.HTML)
            await call.answer()
        else:
            await call.message.answer("😭 Ой, кажется, вас нет в базе!", reply_markup=return_to_start())
            await call.answer()