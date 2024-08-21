from constants.database_tables import Tables

UPDATE_EMPLOYEE_ACTIVITY = f'''
    UPDATE {Tables.SCHEMA}.{Tables.EMPLOYEE}
    SET is_active = %(is_active)s
    WHERE phone = %(phone)s;
'''
UPDATE_POSITION_ID_DEPARTMENT_ID_EMPLOYEE = f'''
    UPDATE {Tables.SCHEMA}.{Tables.EMPLOYEE}
    SET position_id = %(position_id)s,
        department_id = %(department_id)s,
        is_active = TRUE
    WHERE phone = %(phone)s;
'''
UPDATE_EMPLOYEE_DATA_BY_TELEGRAM_ID = f'''
    UPDATE {Tables.SCHEMA}.{Tables.EMPLOYEE}
    SET username = %(username)s,
        full_name = %(full_name)s
    WHERE telegram_id = %(telegram_id)s;
'''
UPDATE_EMPLOYEE_DATA_BY_PHONE = f'''
    UPDATE {Tables.SCHEMA}.{Tables.EMPLOYEE}
    SET telegram_id = %(telegram_id)s,
        username = %(username)s,
        full_name = %(full_name)s,
        last_name = %(last_name)s,
        first_name = %(first_name)s
    WHERE phone = %(phone)s;
'''
UPDATE_EXECUTOR_IN_CURRENT_REQUEST = f'''
    UPDATE {Tables.SCHEMA}.{Tables.REQUEST}
    SET executor_telegram_id = %(executor_telegram_id)s
    WHERE department_id = %(department_id)s
    AND bitrix_deal_id = %(bitrix_deal_id)s;
'''
UPDATE_PHOTO_AND_REPORT_IN_REQUEST = f'''
    UPDATE {Tables.SCHEMA}.{Tables.REQUEST}
    SET executor_photo = %(executor_photo)s,
        report = %(report)s,
        status_id = 4
    WHERE department_id = %(department_id)s
    AND bitrix_deal_id = %(bitrix_deal_id)s;
'''
UPDATE_STATUS_ID_IN_CURRENT_REQUEST = f'''
    UPDATE {Tables.SCHEMA}.{Tables.REQUEST}
    SET status_id = %(status_id)s
    WHERE department_id = %(department_id)s
    AND bitrix_deal_id = %(bitrix_deal_id)s;
'''
UPDATE_REPORT_IN_CURRENT_REQUEST = f'''
    UPDATE {Tables.SCHEMA}.{Tables.REQUEST}
    SET report = %(report)s
    WHERE department_id = %(department_id)s
    AND bitrix_deal_id = %(bitrix_deal_id)s;
'''
UPDATE_EXECUTOR_IN_REQUESTS = f'''
    UPDATE {Tables.SCHEMA}.{Tables.REQUEST}
    SET executor_telegram_id = %(executor_telegram_id)s
    WHERE executor_telegram_id = %(executor_telegram_id)s;
'''
UPDATE_CREATOR_IN_REQUESTS = f'''
    UPDATE {Tables.SCHEMA}.{Tables.REQUEST}
    SET creator_telegram_id = %(creator_telegram_id)s
    WHERE creator_telegram_id = %(creator_telegram_id)s;
'''
