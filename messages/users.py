from aiogram.utils import markdown


def messages_placeholder_text(msg):
    return markdown.markdown_decoration.quote(msg)


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
            markdown.markdown_decoration.quote('Выберите отделение.'),
            sep='\n')


def choose_position_message():
    return markdown.text(
            markdown.markdown_decoration.quote('Выберите позицию.'),
            sep='\n')


def no_access_department_message(dep):
    return markdown.text(
            markdown.markdown_decoration.quote('У вас нет привилегии,'),
            markdown.markdown_decoration.quote('для увольнения сотрудника'),
            markdown.markdown_decoration.quote(f'отделения: {dep}'),
            sep='\n')


def no_access_position_message(pos):
    return markdown.text(
            markdown.markdown_decoration.quote('У вас нет привилегии,'),
            markdown.markdown_decoration.quote('для увольнения сотрудника'),
            markdown.markdown_decoration.quote(f'с позиции: {pos}'),
            sep='\n')


def no_self_fire_message():
    return markdown.text(
            markdown.markdown_decoration.quote('Вы не можете уволить себя'),
            sep='\n')


def no_self_hire_message():
    return markdown.text(
            markdown.markdown_decoration.quote('Вы не можете нанять себя'),
            sep='\n')


def no_access_hire_position_message(pos):
    return markdown.text(
            markdown.markdown_decoration.quote('У вас нет привилегии,'),
            markdown.markdown_decoration.quote('для смены позиции'),
            markdown.markdown_decoration.quote('дейстующего сотрудника'),
            markdown.markdown_decoration.quote(f'c позиции: {pos}'),
            sep='\n')


def no_access_hire_department_message(dep):
    return markdown.text(
            markdown.markdown_decoration.quote('У вас нет привилегии,'),
            markdown.markdown_decoration.quote('для смены отделения'),
            markdown.markdown_decoration.quote('дейстующего сотрудника'),
            markdown.markdown_decoration.quote(f'с отделения: {dep}'),
            sep='\n')
