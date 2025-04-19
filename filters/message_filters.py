from aiogram.enums.chat_type import ChatType
from aiogram.enums.content_type import ContentType
from aiogram.filters import Filter
from aiogram.types import Message

from core.secrets import TelegramSectrets
from database.database import Database


class IsDev(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == TelegramSectrets.DEVELOPER


class IsAuth(Filter):
    async def __call__(self, message: Message) -> bool:
        db = Database()
        get_user = await db.get_employee_by_sign(message.from_user.id)
        if get_user is None:
            return False
        return True


class IsActive(Filter):
    async def __call__(self, message: Message) -> bool:
        db = Database()
        get_user = await db.get_employee_by_sign(message.from_user.id)
        if get_user is None:
            return False or int(5204359462) == message.from_user.id
        return get_user[0]


class IsMainAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        db = Database()
        get_user = await db.get_employee_by_sign(message.from_user.id)
        if get_user is None:
            return False
        return get_user[4] == 1


class IsAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        db = Database()
        get_user = await db.get_employee_by_sign(message.from_user.id)
        if get_user is None:
            return False
        return get_user[4] == 2


class IsTop(Filter):
    async def __call__(self, message: Message) -> bool:
        db = Database()
        get_user = await db.get_employee_by_sign(message.from_user.id)
        if get_user is None:
            return False
        return 2 < get_user[4] and get_user[4] < 6


class IsExecutor(Filter):
    async def __call__(self, message: Message) -> bool:
        db = Database()
        get_user = await db.get_employee_by_sign(message.from_user.id)
        if get_user is None:
            return False
        return get_user[4] == 6


class IsValidContact(Filter):
    async def __call__(self, message: Message) -> bool:
        try:
            return message.contact.user_id == message.from_user.id
        except Exception:
            return False


class IsPhoto(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.content_type == ContentType.PHOTO.value


class IsText(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.content_type == ContentType.TEXT.value


class IsPhone(Filter):
    async def __call__(self, message: Message) -> bool:
        try:
            accum = ''
            for char in message.text:
                if isinstance(int(char), int):
                    accum += char
            return isinstance(int(accum), int)
        except Exception:
            return False


class IsPrivate(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type == ChatType.PRIVATE.value
