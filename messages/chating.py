from aiogram.enums.chat_type import ChatType
from aiogram.types import Message
from aiogram.utils import markdown


def message_placeholder(
        message: Message, users_data, text, message_id, chat_id):
    (
        is_active,
        telegram_id,
        username,
        full_name,
        position_id,
        pos_name,
        department_id,
        dep_name,
        phone,
        last_name,
        first_name
    ) = users_data
    code_info = markdown.text(
        markdown.markdown_decoration.quote('код:'),
        markdown.markdown_decoration.code(f'{message_id}/{chat_id}'))
    if message.chat.type != ChatType.PRIVATE:
        sender_obj = markdown.text(
            markdown.markdown_decoration.quote('группа:'),
            markdown.markdown_decoration.quote(message.chat.title))
        code_info += f'\n{sender_obj}'
    basic_info = markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote('сотрудник:'),
            markdown.markdown_decoration.quote(f'{last_name} {first_name}')),
        markdown.text(
            markdown.markdown_decoration.quote('телефон:'),
            markdown.markdown_decoration.code(phone)),
        markdown.text(
            markdown.markdown_decoration.quote('позиция:'),
            markdown.markdown_decoration.quote(pos_name)),
        markdown.text(
            markdown.markdown_decoration.quote('сообщение:'),
            markdown.markdown_decoration.quote(text)),
        sep='\n')
    return f'{code_info}\n{basic_info}'
