from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, FSInputFile
from keyboards.inline import return_to_start

pvr_router = Router()

@pvr_router.callback_query(F.data == "pvr_pressed")
async def pvr_report(call:CallbackQuery):
    document = FSInputFile("content/sst_ff_pvr.pdf")
    await call.message.answer_document(document,
                                caption="📄 <u>Правила внутреннего распорядка ССТ Финансового факультета</u>",
                                request_timeout=300,
                                reply_markup=return_to_start(),
                                parse_mode=ParseMode.HTML)
    await call.answer()