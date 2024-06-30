from dataclasses import dataclass
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@dataclass(frozen=True)
class ReplyKeyboard:
    ...


@dataclass(frozen=True)
class InlineKeyboard:
    confirm_yes_no = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Да', callback_data='accept'),
             InlineKeyboardButton(text='Нет', callback_data='reject')]
        ]
    )

    confirm_yes_no_cancel = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Да', callback_data='accept'),
             InlineKeyboardButton(text='Нет', callback_data='reject')],
            [InlineKeyboardButton(text='Отмена', callback_data='cancel')]
        ]
    )

    cancel = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Отмена', callback_data='cancel')]
        ]
    )

    update_cancel_skip = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Пропустить', callback_data='skip'),
             InlineKeyboardButton(text='Отмена', callback_data='cancel')]
        ]
    )


reply_keyboard = ReplyKeyboard()
inline_keyboard = InlineKeyboard()
