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
    FINDREQUEST = '🔍 Найти заявку'


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


class DepartmentFloor(Enum):
    MINUSONE = '📃 -1 Этаж'
    ONE = '📃 1 Этаж'
    TWO = '📃 2 Этаж'
    THREE = '📃 3 Этаж'
    ROOF = '📃 Крыша'
    TERRITORY = '📃 Территория объекта'
    OTHER = '📃 Общие помещения'


class CreateZoneKeyboard:
    AREAS = {
        1: None,
        2: None,
        3: None,
        4: {
            DepartmentFloor.MINUSONE.value: {
                'КЕ': 1582,
                'Тех.Зона': 1584,
                'БК': 1586,
                'Холл': 1588,
                'СПА-Салон': 1590
            },
            DepartmentFloor.ONE.value: {
                'ОП': 480,
                'Кухня': 1592,
                'Холл(Ресеп)': 1594,
                'Туалет Гостевой': 1596,
                'Ресторан': 1598,
                'Бассейны': 1600
            },
            DepartmentFloor.TWO.value: {
                'СКДК': 1602,
                'Коридор': 1604,
                'Игровая комната': 1606,
                'Туалет ДК': 1608,
                'Учебный класс': 1610,
                'Раздевалка общая': 1612,
                'Раздевалка мужская': 1614,
                'Раздевалка женская': 1616,
                'Раздевалка мальчики': 1618,
                'Раздевалка девочки': 1620
            },
            DepartmentFloor.THREE.value: {
                'ТЗ': 1622,
                'Туалеты': 1624,
                'ГП1': 1626,
                'ГП2': 1628,
                'YOGA': 1630,
                'CYCLE': 1632
            },
            DepartmentFloor.TERRITORY.value: {
                'Улица': 1634
            },
            DepartmentFloor.OTHER.value: {
                'Лестница техническая': 1636,
                'Лестница клиентская': 1638,
                'Лифт': 1640
            }
        },
        5: None
    }

    def __init__(self, department_id):
        self.department_id = int(department_id)

    async def get_floors_dict(self):
        return self.AREAS[self.department_id]

    async def get_floor_area_dict(self, floor):
        return self.AREAS[self.department_id][floor]
