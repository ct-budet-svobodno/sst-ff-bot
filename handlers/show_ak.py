from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from database.engine import get_session
from database.crud import get_all_activists, is_it_activist
from handlers.start import admin_list
from keyboards.inline import return_to_start

show_ak_router = Router()

async def generate_post(session):
    all_activists = await get_all_activists(session)

    messages = []
    if all_activists is None:
        answer="К сожалению, база данных пуста ૮₍ ´ ꒳ `₎ა"
        messages.append(answer)
        return messages
        
    current_chunk = "📋 <u>БЫЛЛЫ, АЧИВКИ И КОСЯКИ</u>\n\n"
    
    for idx, user in enumerate(all_activists, start=1):
        if user.ach_kos == None:
                user.ach_kos =  "🫥 Пока не получено"
        user_line = (
            f"{idx}. <b>{user.name}</b>\n"
            f" ├ Статус: {user.status}\n"
            f" ├ Telegram ID: {user.telegram_id}\n"
            f" ├ Баллы: <b>{user.score}</b>\n"
            f" └ Последние ачивки и косяки: {user.ach_kos}\n\n"
        )
            
        if len(current_chunk) + len(user_line) > 4000:
            messages.append(current_chunk)
            current_chunk = user_line
        else:
            current_chunk += user_line
    if current_chunk:
        messages.append(current_chunk)
    return messages

@show_ak_router.callback_query(F.data == "show_ak_pressed")
async def full_ak_report(call:CallbackQuery):
    async for session in get_session():
            tgid = call.from_user.username if call.from_user.username[0]=='@' else '@' + call.from_user.username 
            uid = call.from_user.id
            test = await is_it_activist(session, tgid)
            if uid in admin_list:
                test = True
            if test:
                report_chunks = await generate_post(session)
                for chunk in report_chunks:
                    await call.message.answer(
                    text=chunk, 
                    parse_mode=ParseMode.HTML
                )
                await call.message.answer("Кнопка возврата", reply_markup=return_to_start())
                await call.answer()
            else: 
                await call.message.answer("😭 Вы не админ. К сожалению, вы не можете смотреть баллы, ачивки и косяки активистов.", reply_markup=return_to_start())
                await call.answer()