from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
# from sqlalchemy.ext.asyncio import AsyncSession
from keyboards.inline import return_to_start
from database.crud import add_activist
from database.engine import get_session

adact_router = Router()

class Activist_maker(StatesGroup):
    name = State()
    status = State()
    tgid = State()
    birthday = State()
    student_group = State()
    number = State()
    email = State()
    studak = State()
    others = State()
    score = State()

@adact_router.callback_query(F.data == "add_act_pressed")
async def add_act_report(call:CallbackQuery, state:FSMContext):
    await call.message.answer("🌸 Введите фамилию и имя активиста: ")
    await call.answer()
    await state.set_state(Activist_maker.name)

@adact_router.message(Activist_maker.name, F.text)
async def add_name(message:types.Message, state:FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сохранено!🌸\nВведите статус активиста('активист' или 'друг'): ")
    await state.set_state(Activist_maker.status)

@adact_router.message(Activist_maker.status, F.text)
async def add_birthday(message:types.Message, state:FSMContext):
    await state.update_data(status=message.text)
    await message.answer('Сохранено!🌸\nВведите имя пользователя Telegram активиста: ')
    await state.set_state(Activist_maker.tgid)

@adact_router.message(Activist_maker.tgid, F.text)
async def add_nvk_mark(message:types.Message, state:FSMContext):
    await state.update_data(tgid=message.text)
    await message.answer("Сохранено!🌸\nВведите дату рождения активиста в формате 'YYYY-MM-DD' (год-месяц-день): ")
    await state.set_state(Activist_maker.birthday)

@adact_router.message(Activist_maker.birthday, F.text)
async def add_nvk_mark(message:types.Message, state:FSMContext):
    await state.update_data(birthday=message.text)
    await message.answer("Сохранено!🌸\nВведите учебную группу активиста: ")
    await state.set_state(Activist_maker.student_group)

@adact_router.message(Activist_maker.student_group, F.text)
async def add_nvk_mark(message:types.Message, state:FSMContext):
    await state.update_data(student_group=message.text)
    await message.answer("Сохранено!🌸\nВведите номер телефона активиста: ")
    await state.set_state(Activist_maker.number)

@adact_router.message(Activist_maker.number, F.text)
async def add_nvk_mark(message:types.Message, state:FSMContext):
    await state.update_data(number=message.text)
    await message.answer("Сохранено!🌸\nВведите email активиста: ")
    await state.set_state(Activist_maker.email)

@adact_router.message(Activist_maker.email, F.text)
async def add_nvk_mark(message:types.Message, state:FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Сохранено!🌸\nВведите номер студенческого билета активиста: ")
    await state.set_state(Activist_maker.studak)

@adact_router.message(Activist_maker.studak, F.text)
async def add_nvk_mark(message:types.Message, state:FSMContext):
    await state.update_data(studak=message.text)
    await message.answer("Сохранено!🌸\nСостоит ли активист в других подразделениях? Если да, перечислите. Если нет, введите 'нет'.")
    await state.set_state(Activist_maker.others)

@adact_router.message(Activist_maker.others, F.text)
async def add_nvk_mark(message:types.Message, state:FSMContext):
    await state.update_data(from_nvk=message.text)
    await message.answer("Сохранено!...")
    activist = await state.get_data()
    na = activist.get('name')
    st = activist.get('status')
    tgid = activist.get('telegram_id')
    bd = activist.get('birthday')
    sg = activist.get('student_group')
    nu = activist.get('number')
    em = activist.get('email')
    stu = activist.get('studak')
    ot = activist.get('others')
    async for session in get_session():
        user_already_exists = await add_activist(session, na, st, tgid, bd, sg, nu, em, stu, ot)
        if user_already_exists:
            await message.answer("Кажется, активист уже существует в базе!📍")
        else:
            await message.answer("Активист успешно добавлен в базу!✅")