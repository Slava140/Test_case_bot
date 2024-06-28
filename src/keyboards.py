from dataclasses import dataclass
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@dataclass(frozen=True)
class ReplyKeyboard:
    ...


@dataclass(frozen=True)
class InlineKeyboard:
    confirm = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Да', callback_data='accept'),
             InlineKeyboardButton(text='Нет', callback_data='reject')]
        ]
    )


reply_keyboard = ReplyKeyboard()
inline_keyboard = InlineKeyboard()
