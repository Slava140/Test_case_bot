from string import whitespace

from aiogram.types import Message


def name_validator(message: Message):
    text = message.text
    if not (
            2 <= len(text) <= 50 and
            text.isalpha() and
            not text.startswith('/')):
        return False
    return text


def price_validator(message: Message):
    text = message.text
    if not text.isdigit():
        return False
    return int(text)


def id_validator(message: Message):
    text = message.text
    if not text.isdigit():
        return False
    return int(text)
