from string import whitespace

from aiogram.types import Message


def name_validator(message: Message):
    processed_text = message.text.strip(whitespace)
    return all(
        (
            2 <= len(processed_text) <= 50,
            processed_text.isalpha(),
            not processed_text.startswith('/')
        )
    )


def price_validator(message: Message):
    processed_text = message.text.strip()
    if not processed_text.isdigit():
        return False
    return int(processed_text) > 0


def id_validator(message: Message):
    processed_text = message.text.strip()
    if not processed_text.isdigit():
        return False
    return int(processed_text) > 0
