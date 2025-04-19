from enum import Enum


class Department(Enum):
    DYL = [
        '🖥 4Daily', 'https://']
    MSK = [
        '🖥 Московский', 'https://ohanamsk.bitrix24.ru/rest/59/']
    # ('https://ohanamsk.bitrix24.ru/rest/59/'
    # f'{BitrixSecrets.MSK_TOKEN}')]
    VLK = [
        '🖥 Волковский', 'https://ohanafitness.bitrix24.ru/rest/407/']
    # ('https://ohanafitness.bitrix24.ru/rest/407/'
    # f'{BitrixSecrets.VLK_TOKEN}')]
    NKR = [
        '🖥 Некрасовка', 'https://ohananekrasovka.bitrix24.ru/rest/88/']
    # ('https://ohananekrasovka.bitrix24.ru/rest/88/'
    # f'{BitrixSecrets.NKR_TOKEN}')]
    BTV = [
        '🖥 Бунинская', 'https://ohanabutovo.bitrix24.ru/rest/41/']
    # ('https://ohanabutovo.bitrix24.ru/rest/41/'
    # f'{BitrixSecrets.BTV_TOKEN}')]


class Position(Enum):
    MAINADMIN = 'Главный администратор'
    ADMIN = '💻 Администратор'
    TECHAUDIT = '🕵️ Ревизор'
    TOPMGR = '🌟 Топ-сотрудник'
    MGR = '👨‍💼 Сотрудник клуба'
    EMPLOYEE = '👨‍🔧 Техник'


class RequestStatus(Enum):
    NEW = 'Новая заявка'
    ONTECH = 'В работе у техника'
    ONMGR = 'В работе у МЭО'
    HANGON = 'Зависшая'
    DONE = 'Завершена'


class BitrixAccount(Enum):
    DYL = [1, 1, 1, 1]
    MSK = [2, 10689, 11815, 11805]
    VLK = [3, 3967, 425, 127]
    NKR = [4, 25448, 14, 24654]
    BTV = [5, 2921, 2919, 2909]


class BitrixFields(Enum):
    DYL = [
        1, 'UF_CRM_1', 'UF_CRM_2', 'UF_CRM_3', 'UF_CRM_4', 'UF_CRM_5',
        'UF_CRM_1681809686676']
    MSK = [
        2, 'UF_CRM_1681808233117', 'UF_CRM_1681808401521',
        'UF_CRM_1681808510908', 'UF_CRM_1681808569477', 'UF_CRM_1695672376',
        'UF_CRM_1681809686676']
    VLK = [
        3, 'UF_CRM_1681808233117', 'UF_CRM_1681808401521',
        'UF_CRM_1681808510908', 'UF_CRM_1681808569477', 'UF_CRM_1695672392',
        'UF_CRM_1681809686676']
    NKR = [
        4, 'UF_CRM_1681808233117', 'UF_CRM_1681808401521',
        'UF_CRM_1681808510908', 'UF_CRM_1681808569477', 'UF_CRM_1695672383',
        'UF_CRM_1681809686676']
    BTV = [
        5, 'UF_CRM_1681808233117', 'UF_CRM_1681808401521',
        'UF_CRM_1681808510908', 'UF_CRM_1681808569477', 'UF_CRM_1695672396',
        'UF_CRM_1681809686676']


class BitrixStage(Enum):
    DYL = [1, 33, 'NEW', 'PREPARATION', 'PREPAYMENT_INVOIC', 'WON']
    MSK = [2, 33, 'NEW', 'PREPARATION', 'PREPAYMENT_INVOIC', 'WON']
    VLK = [3, 125, 'NEW', 'PREPARATION', 'PREPAYMENT_INVOI', 'WON']
    NKR = [4, 22, 'NEW', 'PREPARATION', 'PREPAYMENT_INVOIC', 'WON']
    BTV = [5, 21, 'NEW', 'PREPARATION', 'PREPAYMENT_INVOIC', 'WON']
