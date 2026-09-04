from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.enums import ParseMode
from keyboards.inline import return_to_start

digest_router = Router()

@digest_router.callback_query(F.data == "digest_pressed")
async def digest_report(call:CallbackQuery):
    document = FSInputFile("content/sst_ff_digest.pdf")
    await call.message.answer_document(document,
                                caption="📆 <u>Дайджест на август</u> (потому что разраб тоже должен развлекаться)",
                                request_timeout=300,
                                reply_markup=return_to_start(),
                                parse_mode=ParseMode.HTML)
    await call.answer()