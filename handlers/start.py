from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from keyboards.inline import get_start_keyboard, admin_start_keyboard
from database.engine import get_session


start_router = Router()
admin_list = [2131378607, 816800090, 1442556368, 988310369]

@start_router.message(Command("start"))
@start_router.callback_query(F.data == "start_pressed")
async def start_handler(event: Message | CallbackQuery):
    async for session in get_session():
        if event.from_user.id in admin_list:
            if isinstance(event, CallbackQuery):
                await event.message.answer(
                    "Привет, админ! Это бот актива ССТ ФФ! 🤖\nВот, что я могу:", 
                    reply_markup=admin_start_keyboard())
                await event.answer()
            else: 
                await event.answer(
                    "Привет, админ! Это бот актива ССТ ФФ! 🤖\nВот, что я могу:", 
                    reply_markup=admin_start_keyboard())
        else:
            if isinstance(event, CallbackQuery):
                await event.message.answer(
                    "Привет! Это бот актива ССТ ФФ! 🤖\nВот, что я могу:", 
                    reply_markup=get_start_keyboard())
                await event.answer()
            else: 
                await event.answer(
                    "Привет! Это бот актива ССТ ФФ! 🤖\nВот, что я могу:", 
                    reply_markup=get_start_keyboard())