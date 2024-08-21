from aiogram.utils import markdown


def unauth_greeting_message(name):
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote('Приветствую,'),
            f'{markdown.bold(name)} '),
        markdown.markdown_decoration.quote('Пройдите регистрацию, для этого'),
        markdown.text(
            markdown.markdown_decoration.quote('нажмите на кнопку:'),
            f'{markdown.bold("Отправить контакт")}'),
        sep='\n')


def contact_success():
    return markdown.text(
            markdown.markdown_decoration.quote('Контакт принят!'),
            sep='\n')


def enter_last_name():
    return markdown.text(
            markdown.markdown_decoration.quote('Введите фамилию'),
            sep='\n')


def enter_first_name():
    return markdown.text(
            markdown.markdown_decoration.quote('Введите имя'),
            sep='\n')


def wrong_full_name():
    return markdown.text(
            markdown.markdown_decoration.quote(
                'Введите личные данные корректно!'),
            sep='\n')


def auth_success():
    return markdown.text(
            markdown.markdown_decoration.quote('Регистрация прошла успешно!'),
            sep='\n')


def auth_employee_pos_and_dep_message(
        position,
        department,
        last_name,
        first_name):
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote('Пользователь:'),
            f'{markdown.bold(last_name)}',
            f'{markdown.bold(first_name)}'),
        markdown.text(
            markdown.markdown_decoration.quote('Отделение:'),
            f'{markdown.bold(department)}'),
        markdown.text(
            markdown.markdown_decoration.quote('Позиция:'),
            f'{markdown.bold(position)}'),
        sep='\n')


def auth_employee_no_dep_and_pos_message():
    return markdown.text(
            markdown.markdown_decoration.quote('Вам не назначена позиция'),
            markdown.markdown_decoration.quote('и отделение для работы.'),
            markdown.markdown_decoration.quote(
                'Администратору или Топ-сотруднику,'),
            markdown.markdown_decoration.quote(
                'необходимо добавить эти данные в'),
            markdown.markdown_decoration.quote('вашу учётную запись.'),
            sep='\n')


def auth_employee_wrong_contact_message():
    return markdown.text(
            markdown.markdown_decoration.quote('Неверные данные!'),
            markdown.text(
                markdown.markdown_decoration.quote('Воспользуйтесь кнопкой:'),
                f'{markdown.bold("Отправить контакт")}'),
            sep='\n')
