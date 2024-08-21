from typing import Union

import emoji
from aiogram.enums.content_type import ContentType
from aiogram.types import Message


def fullname_validator(message: Message) -> Union[str, bool]:
    if message.content_type != ContentType.TEXT.value:
        return False
    text_input = ''.join(message.text.strip().split())
    sym = [
        '-', '+', '^', '*', '/', '\\', '=', '_', '`', '~', '@', '$',
        ':', '?', '&', '%', '#', '"', '(', '{', '[', ']', '}', ')',
        '"', '!', ';', '<', '>', '«', '»', '1', '2', '3', '4', '5',
        '6', '7', '8', '9', '0'
    ]
    result_text = text_input
    for char in text_input:
        if char in sym:
            result_text = result_text.replace(char, '')
        if ':' in emoji.demojize(char):
            result_text = result_text.replace(char, '')
    if len(result_text) > 99:
        return False
    return result_text.capitalize()
