
from aiogram.types import(
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButtonPollType,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder,InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
class Pagination(CallbackData,prefix="pag"):
    action:str
    page:int
def paginator(page:int=0)   :
    builder = InlineKeyboardBuilder()
    builder.row(
    InlineKeyboardButton(text="⬅️",callback_data=Pagination(action="prev", page=page).pack()),
    InlineKeyboardButton(text="➡️",callback_data=Pagination(action="next", page=page).pack()),
        width=2)

    return builder.as_markup(resize_keyboard=True)  