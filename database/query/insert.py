from constants.database_tables import Tables

INSERT_INTO_EMPLOYEE_HIRE = f'''
    INSERT INTO {Tables.SCHEMA}.{Tables.EMPLOYEE} (
        is_active,
        telegram_id,
        username,
        full_name,
        last_name,
        first_name,
        position_id,
        department_id,
        phone)
    VALUES (
        TRUE,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        %(position_id)s,
        %(department_id)s,
        %(phone)s);
'''
INSERT_INTO_EMPLOYEE = f'''
    INSERT INTO {Tables.SCHEMA}.{Tables.EMPLOYEE} (
        telegram_id,
        username,
        full_name,
        last_name,
        first_name,
        position_id,
        department_id,
        phone)
    VALUES (
        %(telegram_id)s,
        %(username)s,
        %(full_name)s,
        %(last_name)s,
        %(first_name)s,
        NULL,
        NULL,
        %(phone)s);
'''
INSERT_INTO_REQUEST = f'''
    INSERT INTO {Tables.SCHEMA}.{Tables.REQUEST} (
        bitrix_deal_id,
        department_id,
        status_id,
        creator_telegram_id,
        creator_photo,
        short_description,
        detailed_description)
    VALUES (
        %(bitrix_deal_id)s,
        %(department_id)s,
        %(status_id)s,
        %(creator_telegram_id)s,
        %(creator_photo)s,
        %(short_description)s,
        %(detailed_description)s);
'''
