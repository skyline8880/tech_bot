from enum import Enum


class CreatorButtons(Enum):
    HIRE = '👥 Принять'
    FIRE = '👥 Уволить'
    REQUEST = '📑 Работа с заявками'
    STAT = '📊 Статистика'
    REPORT = '📊 Выгрузка отчётов'


class RequestButtons(Enum):
    CREATEREQUEST = '➕ Создать заявку'
    MYREQUESTS = '📑 Мои заявки'
    REQUESTLIST = '📄 Список заявок'


class ExecutorButtons(Enum):
    MYREQUESTS = '📑 Мои заявки'
    REQUESTLIST = '📄 Список заявок'


class ActionButtons(Enum):
    CANCEL = '❌ Отмена'
    MENU = '☰ Меню'
    BACK = '🔙 Назад'


class CurrentRequestActionButtons(Enum):
    INROLE = '🛠 Взять в работу'
    HANDOVERMGR = '🔝 Передать в работу МЭО'
    HANGON = '💤 Зависшая заявка'
    DONE = '☑️ Завершить'
