from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.enums import ParseMode
# from aiogram.utils.media_group import MediaGroupBuilder
from keyboards.inline import return_to_start

ak_router = Router()

@ak_router.callback_query(F.data == "ak_pressed")
async def ak_report(call:CallbackQuery):
    # album = MediaGroupBuilder(caption="🌟 Ачивки и косяки")
    # file_paths = [
    #     "content/sst_ff_ak1",
    #     "content/sst_ff_ak2"
    # ]
    # for path in file_paths:
    #     album.add_photo(media=FSInputFile(path))
    await call.message.answer("🌟 <u>Ачивки и косяки</u>\n\n<a href='https://drive.google.com/file/d/1UGTodCiQnPsPdx-SNOPd2-qZpPVcZDyS/view?usp=sharing'>ССЫЛКА</a>",
                                request_timeout=300,
                                reply_markup=return_to_start(),
                                parse_mode=ParseMode.HTML)
    await call.answer()