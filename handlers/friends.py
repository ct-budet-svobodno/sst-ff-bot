from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, FSInputFile
# from sqlalchemy.ext.asyncio import AsyncSession
from keyboards.inline import return_to_start
# from database.crud import is_it_nvk, get_all_activists

friends_router = Router()

@friends_router.callback_query(F.data == "friends_pressed")
async def friends_report(call:CallbackQuery):
    document = FSInputFile("content/sst_ff_friends.pdf")
    await call.message.answer_document(document,
                                caption="📜 <u>Положение о статусе друзей</u>",
                                request_timeout=300,
                                reply_markup=return_to_start(),
                                parse_mode=ParseMode.HTML)
    await call.answer()