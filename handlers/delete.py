from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
# from sqlalchemy.ext.asyncio import AsyncSession
from keyboards.inline import return_to_start, assurance
from database.crud import delete_activist
from database.engine import get_session

delete_router = Router()

class Activist_delete(StatesGroup):
    tgid = State()
    assurance = State()

@delete_router.callback_query(F.data == "delete_pressed")
async def delete_report(call:CallbackQuery, state:FSMContext):
    await call.message.answer("🥀 Введите имя пользователя Telegram активиста: ")
    await call.answer()
    await state.set_state(Activist_delete.tgid)

@delete_router.message(Activist_delete.tgid, F.text)
async def assurance_clarify(message:types.Message, state:FSMContext):
    await state.update_data(tgid=message.text)
    await message.answer(f'🥀 Вы точно уверены, что хотите удалить активиста {message.text}?', reply_markup=assurance())
    await state.set_state(Activist_delete.assurance)

@delete_router.callback_query(Activist_delete.assurance, F.data == "final_stage_pressed")
async def add_birthday(call:CallbackQuery, state:FSMContext):
    await state.update_data(assurance=call.data)
    await call.message.answer('Сохранено!...')
    activist = await state.get_data()
    tgid = activist.get('tgid')
    async for session in get_session():
        deleting = await delete_activist(session, tgid)
        if deleting:
            await call.message.answer("Активист успешно удален!✅", reply_markup=return_to_start())
            await call.answer()
        else:
            await call.message.answer("Кажется, активиста, которого вы пытаетесь удалить, не существует!📍", reply_markup=return_to_start())
            await call.answer()