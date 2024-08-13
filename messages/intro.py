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


def auth_success():
    return markdown.text(
            markdown.markdown_decoration.quote('Регистрация прошла успешно!'),
            sep='\n')


def auth_employee_pos_and_dep_message(
        position,
        department):
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote('Локация:'),
            f'{markdown.bold(department)}'),
        markdown.text(
            markdown.markdown_decoration.quote('Позиция:'),
            f'{markdown.bold(position)}'),
        sep='\n')


def auth_employee_no_dep_and_pos_message():
    return markdown.text(
            markdown.markdown_decoration.quote('Вам не назначена позиция'),
            markdown.markdown_decoration.quote('и локация для работы.'),
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
