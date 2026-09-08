from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardMarkup

def get_start_keyboard():
    buttons = [
        [InlineKeyboardButton(text="История", callback_data="history_pressed")],
        [InlineKeyboardButton(text="ПВР", callback_data="pvr_pressed")],
        [InlineKeyboardButton(text="Ачивки и косяки", callback_data="ak_pressed")],
        [InlineKeyboardButton(text="Тьюторское дерево", callback_data="tutr_pressed")],
        [InlineKeyboardButton(text="Положение о статусе друзей", callback_data="friends_pressed")],
        [InlineKeyboardButton(text="Дайджест", callback_data="digest_pressed")],
        [InlineKeyboardButton(text="Контакты", callback_data="contacts_pressed")],
        [InlineKeyboardButton(text="Найти активиста", callback_data="search_pressed")],
        [InlineKeyboardButton(text="Мой рейтинг", callback_data="raiting_pressed")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def admin_start_keyboard():
    buttons = [
        [InlineKeyboardButton(text="История", callback_data="history_pressed")],
        [InlineKeyboardButton(text="ПВР", callback_data="pvr_pressed")],
        [InlineKeyboardButton(text="Ачивки и косяки", callback_data="ak_pressed")],
        [InlineKeyboardButton(text="Тьюторское дерево", callback_data="tutr_pressed")],
        [InlineKeyboardButton(text="Положение о статусе друзей", callback_data="friends_pressed")],
        [InlineKeyboardButton(text="Дайджест", callback_data="digest_pressed")],
        [InlineKeyboardButton(text="Контакты", callback_data="contacts_pressed")],
        [InlineKeyboardButton(text="Найти активиста", callback_data="search_pressed")],
        [InlineKeyboardButton(text="Мой рейтинг", callback_data="raiting_pressed")],
        [InlineKeyboardButton(text="Добавить активиста", callback_data="add_act_pressed")],
        [InlineKeyboardButton(text="Удалить активиста", callback_data="delete_pressed")],
        [InlineKeyboardButton(text="Сменить дайджест", callback_data="change_digest_pressed")],
        [InlineKeyboardButton(text="Список активистов с баллами и ачивками", callback_data="show_ak_pressed")],
        [InlineKeyboardButton(text="Прочая админская магия", callback_data="admin_pressed")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def return_to_start():
    buttons = [
        [InlineKeyboardButton(text="↩️ Вернуться к стартовому меню", callback_data="start_pressed")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def return_or_continue():
    buttons = [
        [InlineKeyboardButton(text="↩️ Вернуться к стартовому меню", callback_data="start_pressed")],
        [InlineKeyboardButton(text="Ввести UID", callback_data="continue_pressed")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def admin_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Изменить баллы активиста", callback_data="change_score_pressed")],
        [InlineKeyboardButton(text="Добавить ачивку или косяк активисту", callback_data="add_ak_pressed")],
        [InlineKeyboardButton(text="Узнать баллы и ачивки активиста", callback_data="info_score_pressed")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def assurance():
    buttons = [
        [InlineKeyboardButton(text="Да", callback_data="final_stage_pressed")],
        [InlineKeyboardButton(text="Нет", callback_data="start_pressed")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard