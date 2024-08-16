import datetime as dt

from aiogram.utils import markdown


def request_action_message(action):
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote('Активность:'),
            f'{markdown.bold(action)}'),
        markdown.markdown_decoration.quote('Выберите действие.'),
        sep='\n')


def request_floor_message():
    return markdown.text(
        markdown.markdown_decoration.quote(
            'Выберите этаж или территорию объекта.'),
        sep='\n')


def request_zone_message():
    return markdown.text(
        markdown.markdown_decoration.quote('Выберите зону неисправности.'),
        sep='\n')


def request_break_type_message():
    return markdown.text(
        markdown.markdown_decoration.quote('Вид неисправности.'),
        sep='\n')


def request_photo_message():
    return markdown.text(
        markdown.markdown_decoration.quote('Сделайте снимок неисправности'),
        markdown.markdown_decoration.quote('и отправьте его боту.'),
        sep='\n')


def request_report_photo_message():
    return markdown.text(
        markdown.markdown_decoration.quote('Сделайте снимок результата,'),
        markdown.markdown_decoration.quote('выполненной работы и отправьте'),
        markdown.markdown_decoration.quote('его боту.'),
        sep='\n')


def request_report_text_message():
    return markdown.text(
        markdown.markdown_decoration.quote('Опишите проделанную работу.'),
        sep='\n')


def request_short_desc_message():
    return markdown.text(
        markdown.markdown_decoration.quote('Введите краткое описание'),
        markdown.markdown_decoration.quote('неисправности.'),
        markdown.markdown_decoration.quote('Оно будет отображаться'),
        markdown.markdown_decoration.quote('как название заявки.'),
        sep='\n')


def request_detailed_desc_message():
    return markdown.text(
        markdown.markdown_decoration.quote('Теперь, опишите неисправность'),
        markdown.markdown_decoration.quote('подробнее.'),
        sep='\n')


def request_wrong_text_message():
    return markdown.text(
        markdown.markdown_decoration.quote('Некорректный формат ввода!'),
        markdown.markdown_decoration.quote(
            'Введите сообщение в формате текста.'),
        sep='\n')


def request_wrong_photo_message():
    return markdown.text(
        markdown.markdown_decoration.quote('Некорректный формат ввода!'),
        markdown.markdown_decoration.quote(
            'Введите файл в формате изображения.'),
        sep='\n')


def bitrix_creat_deal_error_message():
    return markdown.text(
        markdown.markdown_decoration.quote(
            'Ошибка публикации заявки в битрикс!'),
        sep='\n')


def request_detail_message(request_data):
    executor = request_data[21]
    report = request_data[27]
    if executor is None:
        executor = 'Не принят в работу'
    if report is None:
        report = 'Работа не проведена'
    time = dt.datetime.strftime(request_data[28], "%H:%M")
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote('ID сделки:'),
            f'{markdown.bold(request_data[0])}'),
        markdown.text(
            markdown.markdown_decoration.quote('Дата создания:'),
            f'{markdown.bold(request_data[28].date())}',
            f'{markdown.bold(time)}'),
        markdown.text(
            markdown.markdown_decoration.quote('Отделение:'),
            f'{markdown.bold(request_data[2])}'),
        markdown.text(
            markdown.markdown_decoration.quote('Статус:'),
            f'{markdown.bold(request_data[4])}'),
        markdown.text(
            markdown.markdown_decoration.quote('Постановщик:'),
            f'{markdown.bold(request_data[8])}'),
        markdown.text(
            markdown.markdown_decoration.quote('Зона:'),
            f'{markdown.bold(request_data[13])}'),
        markdown.text(
            markdown.markdown_decoration.quote('Вид неисправности:'),
            f'{markdown.bold(request_data[14])}'),
        markdown.text(
            markdown.markdown_decoration.quote('Краткое описание:'),
            f'{markdown.bold(request_data[16])}'),
        markdown.text(
            markdown.markdown_decoration.quote('Детальное описание:'),
            f'{markdown.bold(request_data[17])}'),
        markdown.text(
            markdown.markdown_decoration.quote('Исполнитель:'),
            f'{markdown.bold(executor)}'),
        markdown.text(
            markdown.markdown_decoration.quote('Отчёт:'),
            f'{markdown.bold(report)}'),
        sep='\n')


def request_list_message(position_id, is_own):
    list_type = 'всех'
    if is_own:
        list_type = 'ваших'
    object_relation = 'всем объектам'
    if position_id in (3, 4):
        object_relation = 'вашему объекту'
    return markdown.text(
        markdown.markdown_decoration.quote(
            f'Список {list_type} незавершённых заявок'),
        markdown.markdown_decoration.quote(
            f'по {object_relation}.'),
        sep='\n')


def new_request_message():
    return markdown.text(
        markdown.markdown_decoration.quote(
            '❗️На объекте новая заявка❗️'),
        sep='\n')


def done_request_message():
    return markdown.text(
        markdown.markdown_decoration.quote(
            '❗️Заявка завершена❗️'),
        sep='\n')
