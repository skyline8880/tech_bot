from constants.database_tables import Tables

DELETE_REQUEST = f'''
    DELETE FROM {Tables.SCHEMA}.{Tables.REQUEST}
    WHERE department_id = %(department_id)s
    AND bitrix_deal_id = %(bitrix_deal_id)s
'''
