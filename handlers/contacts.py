from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
# from sqlalchemy.ext.asyncio import AsyncSession
from database.engine import get_session
from database.crud import is_it_activist, get_all_activists
from handlers.start import admin_list
from keyboards.inline import return_to_start

contact_router = Router()

async def generate_post(session):
    all_activists = await get_all_activists(session)

    messages = []
    if all_activists is None:
        answer="К сожалению, база данных пуста ૮₍ ´ ꒳ `₎ა"
        messages.append(answer)
        return messages
        
    current_chunk = "📋 <u>КОНТАКТНАЯ ИНФОРМАЦИЯ</u>\n\n"
    
    for idx, user in enumerate(all_activists, start=1):
        if len(user.station) < 2:
            user.station = "нет информации"
        if len(user.number) < 2:
            user.number = "нет информации"
        user_line = (
            f"{idx}. <b>{user.name}</b>\n"
            f"   ├ Статус: `{user.status}`\n"
            f"   ├ Telegram ID: `{user.telegram_id}`\n"
            f"   ├ Дата рождения: `{user.birthday[:11]}`\n"
            f"   ├ Группа: `{user.student_group}`\n"
            f"   ├ Телефон: `{user.number}`\n"
            f"   ├ Почта: `{user.email}`\n"
            f"   ├ Номер студенческого: `{user.studak}`\n"
            f"   ├ Другие подразделения: `{user.others}`\n"
            f"   └ Метро: {user.station}\n\n"
        )
            
        if len(current_chunk) + len(user_line) > 4000:
            messages.append(current_chunk)
            current_chunk = user_line
        else:
            current_chunk += user_line
    if current_chunk:
        messages.append(current_chunk)
    return messages

@contact_router.callback_query(F.data == "contacts_pressed")
async def db_activists_report(call:CallbackQuery):
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
            await call.message.answer("😭 Вас нет в базе. К сожалению, вы не можете смотреть контакты активистов.", reply_markup=return_to_start())
            await call.answer()