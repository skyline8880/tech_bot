from constants.database_tables import Tables

INSERT_DEPARTMENT = f'''
    INSERT INTO {Tables.SCHEMA}.{Tables.DEPARTMENT} (
        name,
        bitrix_webhook)
    VALUES (
        %(department_name)s,
        %(department_webhook)s);
'''
INSERT_POSITION = f'''
    INSERT INTO {Tables.SCHEMA}.{Tables.POSITION} (
        name)
    VALUES (
        %(position_name)s);
'''
INSERT_REQUEST_STATUS = f'''
    INSERT INTO {Tables.SCHEMA}.{Tables.REQUEST_STATUS} (
        name)
    VALUES (
        %(status_name)s);
'''
INSERT_BITRIX_ACCOUNT = f'''
    INSERT INTO {Tables.SCHEMA}.{Tables.BITRIX_ACCOUNT} (
        department_id,
        tech,
        mgr_tech,
        head_tech)
    VALUES (
        %(department_id)s,
        %(tech)s,
        %(mgr_tech)s,
        %(head_tech)s);
'''
INSERT_BITRIX_FIELD = f'''
    INSERT INTO {Tables.SCHEMA}.{Tables.BITRIX_FIELD} (
        department_id,
        photo,
        short_description,
        detailed_description,
        report)
    VALUES (
        %(department_id)s,
        %(photo)s,
        %(short_description)s,
        %(detailed_description)s,
        %(report)s);
'''
INSERT_BITRIX_STAGE = f'''
    INSERT INTO {Tables.SCHEMA}.{Tables.BITRIX_STAGE} (
        department_id,
        category_id,
        new,
        onmgr,
        hangon,
        done)
    VALUES (
        %(department_id)s,
        %(category_id)s,
        %(new)s,
        %(onmgr)s,
        %(hangon)s,
        %(done)s);
'''
