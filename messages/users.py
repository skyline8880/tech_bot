from aiogram.utils import markdown


def employee_phone_entry_message(action):
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote('Активность:'),
            f'{markdown.bold(action)}'),
        markdown.markdown_decoration.quote('Введите номер сотрудника.'),
        sep='\n')


def employee_wrong_phone_message():
    return markdown.text(
        markdown.markdown_decoration.quote('Некорректный формат ввода!'),
        sep='\n')


def no_employee_phone_message(phone):
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote('Номер:'),
            f'{markdown.code(phone)}'),
        markdown.markdown_decoration.quote('отсутствует в базе.'),
        sep='\n')


def employee_was_fired_message(phone):
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote('Номер:'),
            f'{markdown.code(phone)}'),
        markdown.markdown_decoration.quote('удалён как сотрудник.'),
        sep='\n')


def employee_was_hired_message(phone):
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote('Номер:'),
            f'{markdown.code(phone)}'),
        markdown.markdown_decoration.quote('добавлен как сотрудник.'),
        sep='\n')


def choose_department_message():
    return markdown.text(
            markdown.markdown_decoration.quote('Выберите локацию.'),
            sep='\n')


def choose_position_message():
    return markdown.text(
            markdown.markdown_decoration.quote('Выберите позицию.'),
            sep='\n')
