from aiogram.utils import markdown
from aiogram.utils.formatting import (Bold, as_key_value, as_list,
                                      as_marked_section)

from constants.buttons_init import CreatorButtons
from constants.database_init import RequestStatus


def statistic_message(data):
    data_array = [Bold(CreatorButtons.STAT.value)]
    as_marked_section
    for line in data:
        new, ontech, onmgr, hangon, done = line[2:]
        if new is None:
            new = 0
        if ontech is None:
            ontech = 0
        if onmgr is None:
            onmgr = 0
        if hangon is None:
            hangon = 0
        if done is None:
            done = 0
        if line[0] != 1:
            data_array.append(
                as_marked_section(
                    Bold(f'  {line[1]}'),
                    as_key_value(RequestStatus.NEW.value, Bold(new)),
                    as_key_value(RequestStatus.ONTECH.value, Bold(ontech)),
                    as_key_value(RequestStatus.ONMGR.value, Bold(onmgr)),
                    as_key_value(RequestStatus.HANGON.value, Bold(hangon)),
                    as_key_value(RequestStatus.DONE.value, Bold(done)),
                    marker='      ▪️'))
    return as_list(
        *data_array, sep='\n\n').as_markdown()


def add_reports_period_message():
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote(
                'Введите период в формате: ')),
        markdown.text(
            markdown.markdown_decoration.quote(
                'ДД.ММ.ГГГГ-ДД.ММ.ГГГГ')),
        sep='\n')


def period_reports_nodata(begin, end):
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote(
                f"За период: {begin} - {end}")),
        markdown.text(
            markdown.markdown_decoration.quote(
                "Нет данных!")),
        sep='\n')


def period_reports_data(begin, end):
    return markdown.text(
        markdown.markdown_decoration.quote(f'За период: {begin} - {end}'),
        markdown.markdown_decoration.quote("Отчет готов!"),
        sep='\n')
