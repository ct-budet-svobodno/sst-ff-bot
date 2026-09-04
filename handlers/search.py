from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from database.engine import get_session
from database.crud import is_it_activist, get_rate
from handlers.start import admin_list
from keyboards.inline import return_to_start

search_router = Router()
class Search_steps(StatesGroup):
    tgid = State()

def generate_report(user):
    if len(user.station) < 2:
        user.station = "нет информации"
    if len(user.number) < 2:
        user.number = "нет информации" 
    report = (
            f"🦊<u><b>{user.name}</b></u>\n"
            f"├ Статус: {user.status}\n"
            f"├ Telegram ID: {user.telegram_id}\n"
            f"├ Дата рождения: {user.birthday[:11]}\n"
            f"├ Группа: {user.student_group}\n"
            f"├ Телефон: {user.number}\n"
            f"├ Почта: {user.email}\n"
            f"├ Номер студенческого: {user.studak}\n"
            f"├ Другие подразделения: {user.others}\n"
            f"└ Метро: {user.station}"
    )
    return report

@search_router.callback_query(F.data == "search_pressed")
async def search_report(call:CallbackQuery, state:FSMContext):
    async for session in get_session():
        tgid = call.from_user.username if call.from_user.username[0]=='@' else '@' + call.from_user.username 
        uid = call.from_user.id
        test = await is_it_activist(session, tgid)
        if uid in admin_list:
            test = True
        if test:
            await call.message.answer("Введите имя пользователя Telegram акивиста: ")
            await call.answer()
            await state.set_state(Search_steps.tgid)
        else: 
            await call.message.answer("😭 Вас нет в базе. К сожалению, вы не можете видеть информацию об активистах.", reply_markup=return_to_start())
            await call.answer()

@search_router.message(Search_steps.tgid, F.text)
async def search_report(message:Message, state:FSMContext):
    print("Тг принят!!!")
    async for session in get_session():
        await state.update_data(tgid=message.text)
        search_info = await state.get_data()
        tgid = search_info.get('tgid')
        user = await get_rate(session, tgid)
        if user != None:
            report = generate_report(user)
            await message.answer("<u>АКТУАЛЬНЫЕ ДАННЫЕ</u>\n\n" + report, reply_markup=return_to_start(), parse_mode=ParseMode.HTML)
        else:
            await message.answer("😭 Кажется, что-то пошло не так: активист не найден!", reply_markup=return_to_start())