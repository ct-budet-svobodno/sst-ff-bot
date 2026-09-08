from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
# from sqlalchemy.ext.asyncio import AsyncSession
from config import BOT_TOKEN
from keyboards.inline import return_to_start, admin_keyboard, return_or_continue
from database.engine import get_session
from database.crud import change_score, add_ach_or_kos, get_rate
from .my_raiting import generate_report

admin_router = Router()
bot = Bot(BOT_TOKEN)
class Admin_acts(StatesGroup):
    chosen_act = State()
    tgid = State()
    content = State()
    decision = State()
    uid = State()


@admin_router.callback_query(F.data == "admin_pressed")
async def list_of_admin_acts(call:CallbackQuery, state: FSMContext):
    await call.message.answer("Выберите действие: ", reply_markup=admin_keyboard())
    await call.answer()
    await state.set_state(Admin_acts.chosen_act)

@admin_router.callback_query(Admin_acts.chosen_act, F.data)
async def change_scores(call:CallbackQuery, state: FSMContext):
    await state.update_data(chosen_act=call.data)
    await call.message.answer("Введите имя пользователя Telegram акивиста: ")
    await call.answer()
    await state.set_state(Admin_acts.tgid)

@admin_router.message(Admin_acts.tgid, F.text)
async def change_scores(message:Message, state: FSMContext):
    await state.update_data(tgid=message.text)
    info = await state.get_data()
    if info.get("chosen_act") == "change_score_pressed":
        await message.answer("Теперь введите положительным или отрицательным числом количество баллов," \
                            " которое вы хотите прибавить или отнять у активиста:\n" \
                            "(Пример: 10 - чтобы прибавить 10 баллов, -10 - чтобы отнять)")
    elif info.get("chosen_act") == "add_ak_pressed":
        await message.answer("Теперь введите наименование ачивки или косяка:\n" \
                            "(Пример: Ого, коллеги)")
    elif info.get("chosen_act") == "info_score_pressed":
            await message.answer("Начинаем искать... Пришлите точку или любое другое текстовое сообщение для продолжения 👾")
    await state.set_state(Admin_acts.content)

@admin_router.message(Admin_acts.content, F.text)
async def change_scores(message:Message, state: FSMContext):
    await state.update_data(content=message.text)
    operation = await state.get_data()
    tgid = operation.get('tgid')
    async for session in get_session():
        if operation.get("chosen_act") == "change_score_pressed":
            sc_dif = operation.get('content')
            result = await change_score(session, tgid, sc_dif)
            if result == True:
                await message.answer("🪷 Изменения были успешно сохранены!", reply_markup=return_to_start())
            else:
                await message.answer("😭 Кажется, что-то пошло не так: изменения не были сохранены!", reply_markup=return_to_start())
        elif operation.get("chosen_act") == "add_ak_pressed":
            label = operation.get("content")
            result = await add_ach_or_kos(session, tgid, label)
            if result != False:
                await message.answer("🪷 Изменения сохранены! Список недавних ачивок и косяков активиста: \n" \
                                     f"{result}")
                await message.answer("Чтобы уведомить активиста о полученной ачивке или косяке, укажите его uid" \
                                     " (как узнать UID - <a href='https://dtf.ru/howto/4835984-kak-uznat-telegram-id'>ССЫЛКА</a>)", 
                                     parse_mode=ParseMode.HTML, reply_markup=return_or_continue())
                await state.set_state(Admin_acts.decision)
            else:
                await message.answer("😭 Кажется, что-то пошло не так: изменения не были сохранены!", reply_markup=return_to_start())
        elif operation.get("chosen_act") == "info_score_pressed":
            user = await get_rate(session, tgid)
            if user != None:
                report = generate_report(user.name, user.score, user.ach_kos, user.status)
                await message.answer("<u>АКТУАЛЬНЫЕ ДАННЫЕ</u>\n\n" + report, reply_markup=return_to_start(), parse_mode=ParseMode.HTML)
            else:
                await message.answer("😭 Кажется, что-то пошло не так: активист не найден!", reply_markup=return_to_start())

@admin_router.callback_query(Admin_acts.decision, F.data == "continue_pressed")
async def change_scores(call:CallbackQuery, state: FSMContext):
    await state.update_data(decision=call.data)
    await call.message.answer("Введите UID акивиста: ")
    await call.answer()
    await state.set_state(Admin_acts.uid)

@admin_router.message(Admin_acts.uid, F.text)
async def change_scores(message:Message, state: FSMContext):
    await state.update_data(uid=message.text)
    info = await state.get_data()
    uid = info.get("uid")
    try:
        await bot.send_message(
            chat_id=uid, 
            text="Привет! 🤖 Кажется, ты получил новую ачивку или косяк!\nЗагляни скорее в свой профиль, чтобы узнать, что там."
        )
        await message.answer("Сообщение отправлено!",reply_markup=return_to_start())
    except Exception as e:
        print(f"Не удалось отправить сообщение: {e}")
        await message.answer("Кажется, что-то пошло не так! Не удалось отправить сообщение.",reply_markup=return_to_start())