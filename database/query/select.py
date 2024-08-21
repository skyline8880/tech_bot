from constants.database_tables import Tables

SELECT_DEPERTMENT_BY_SIGN = f'''
    SELECT
        id,
        name,
        bitrix_webhook
    FROM {Tables.SCHEMA}.{Tables.DEPARTMENT}
    WHERE id::VARCHAR = %(department_sign)s OR
        name::VARCHAR = %(department_sign)s;
'''
SELECT_STATUS_BY_SIGN = f'''
    SELECT
        id,
        name
    FROM {Tables.SCHEMA}.{Tables.REQUEST_STATUS}
    WHERE id::VARCHAR = %(status_sign)s OR
        name::VARCHAR = %(status_sign)s;
'''
SELECT_POSITION_BY_SIGN = f'''
    SELECT
        id,
        name
    FROM {Tables.SCHEMA}.{Tables.POSITION}
    WHERE id::VARCHAR = %(position_sign)s OR
        name::VARCHAR = %(position_sign)s;
'''
SELECT_BITRIX_STAGE_BY_DEPARTMENT_ID = f'''
    SELECT
        category_id,
        new,
        onmgr,
        hangon,
        done
    FROM {Tables.SCHEMA}.{Tables.BITRIX_STAGE}
    WHERE department_id = %(department_id)s;
'''
SELECT_BITRIX_FIELD_BY_DEPARTMENT_ID = f'''
    SELECT
        zone,
        break_type,
        photo,
        short_description,
        detailed_description,
        report
    FROM {Tables.SCHEMA}.{Tables.BITRIX_FIELD}
    WHERE department_id = %(department_id)s;
'''
SELECT_BITRIX_ACCOUNT_BY_DEPARTMENT_ID = f'''
    SELECT
        tech,
        mgr_tech,
        head_tech
    FROM {Tables.SCHEMA}.{Tables.BITRIX_ACCOUNT}
    WHERE department_id = %(department_id)s;
'''
SELECT_EMPLOYEE_BY_SIGN = f'''
    SELECT
        emp.is_active,
        emp.telegram_id,
        emp.username,
        emp.full_name,
        emp.position_id,
        pos.name,
        emp.department_id,
        dep.name,
        emp.phone,
        emp.last_name,
        emp.first_name
    FROM {Tables.SCHEMA}.{Tables.EMPLOYEE} AS emp
    LEFT JOIN {Tables.SCHEMA}.{Tables.POSITION} AS pos
    ON emp.position_id = pos.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.DEPARTMENT} AS dep
    ON emp.department_id = dep.id
    WHERE emp.telegram_id::VARCHAR = %(employee_sign)s
    OR emp.phone::VARCHAR = %(employee_sign)s
    OR emp.username::VARCHAR = %(employee_sign)s
    OR emp.full_name::VARCHAR = %(employee_sign)s
'''
SELECT_EXECUTORS_BY_DEPRTMENT_ID = f'''
    SELECT
        telegram_id
    FROM {Tables.SCHEMA}.{Tables.EMPLOYEE}
    WHERE position_id = 4 AND is_active = TRUE
    AND department_id = %(department_id)s
'''
SELECT_REQUESTS = f'''
    SELECT
        req.bitrix_deal_id AS bitrix_deal_id,
        req.department_id AS department_id,
        dep.name AS department_name,
        req.status_id AS status_id,
        rstat.name AS status_name,
        req.creator_telegram_id AS creator_telegram_id,
        cemp.username AS creator_username,
        cemp.full_name  AS creator_full_name,
        cemp.phone AS creator_phone,
        cemp.department_id AS creator_department_id,
        cdep.name AS creator_department,
        cemp.position_id AS creator_position_id,
        cpos.name AS creator_position,
        req.zone AS zone,
        req.break_type AS brake_type,
        req.creator_photo AS creator_photo,
        req.short_description AS short_description,
        req.detailed_description AS detailed_description,
        req.executor_telegram_id AS executor_telegram_id,
        eemp.username AS creator_username,
        eemp.full_name  AS creator_full_name,
        eemp.phone AS creator_phone,
        eemp.department_id AS executor_department_id,
        edep.name AS executor_department,
        eemp.position_id AS executor_position_id,
        epos.name AS executor_position,
        req.executor_photo AS executor_photo,
        req.report AS report,
        req.create_date AS create_date
    FROM {Tables.SCHEMA}.{Tables.REQUEST} AS req
    LEFT JOIN {Tables.SCHEMA}.{Tables.DEPARTMENT} AS dep
    ON req.department_id = dep.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.REQUEST_STATUS} AS rstat
    ON req.status_id = rstat.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.EMPLOYEE} AS cemp
    ON req.creator_telegram_id = cemp.telegram_id
    LEFT JOIN {Tables.SCHEMA}.{Tables.POSITION} AS cpos
    ON cemp.position_id = cpos.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.DEPARTMENT} AS cdep
    ON cemp.department_id = cdep.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.EMPLOYEE} AS eemp
    ON req.executor_telegram_id = eemp.telegram_id
    LEFT JOIN {Tables.SCHEMA}.{Tables.POSITION} AS epos
    ON cemp.position_id = epos.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.DEPARTMENT} AS edep
    ON eemp.department_id = edep.id
    ORDER BY req.create_date;
'''
SELECT_REQUESTS_BY_STATUS = f'''
    SELECT
        req.bitrix_deal_id AS bitrix_deal_id,
        req.department_id AS department_id,
        dep.name AS department_name,
        req.status_id AS status_id,
        rstat.name AS status_name,
        req.creator_telegram_id AS creator_telegram_id,
        cemp.username AS creator_username,
        cemp.full_name  AS creator_full_name,
        cemp.phone AS creator_phone,
        cemp.department_id AS creator_department_id,
        cdep.name AS creator_department,
        cemp.position_id AS creator_position_id,
        cpos.name AS creator_position,
        req.zone AS zone,
        req.break_type AS brake_type,
        req.creator_photo AS creator_photo,
        req.short_description AS short_description,
        req.detailed_description AS detailed_description,
        req.executor_telegram_id AS executor_telegram_id,
        eemp.username AS creator_username,
        eemp.full_name  AS creator_full_name,
        eemp.phone AS creator_phone,
        eemp.department_id AS executor_department_id,
        edep.name AS executor_department,
        eemp.position_id AS executor_position_id,
        epos.name AS executor_position,
        req.executor_photo AS executor_photo,
        req.report AS report,
        req.create_date AS create_date
    FROM {Tables.SCHEMA}.{Tables.REQUEST} AS req
    LEFT JOIN {Tables.SCHEMA}.{Tables.DEPARTMENT} AS dep
    ON req.department_id = dep.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.REQUEST_STATUS} AS rstat
    ON req.status_id = rstat.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.EMPLOYEE} AS cemp
    ON req.creator_telegram_id = cemp.telegram_id
    LEFT JOIN {Tables.SCHEMA}.{Tables.POSITION} AS cpos
    ON cemp.position_id = cpos.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.DEPARTMENT} AS cdep
    ON cemp.department_id = cdep.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.EMPLOYEE} AS eemp
    ON req.executor_telegram_id = eemp.telegram_id
    LEFT JOIN {Tables.SCHEMA}.{Tables.POSITION} AS epos
    ON cemp.position_id = epos.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.DEPARTMENT} AS edep
    ON eemp.department_id = edep.id
    WHERE req.status_id < %(status_id)s
    ORDER BY req.create_date;
'''
SELECT_REQUESTS_BY_DEPARTMENT = f'''
    SELECT
        req.bitrix_deal_id AS bitrix_deal_id,
        req.department_id AS department_id,
        dep.name AS department_name,
        req.status_id AS status_id,
        rstat.name AS status_name,
        req.creator_telegram_id AS creator_telegram_id,
        cemp.username AS creator_username,
        cemp.full_name  AS creator_full_name,
        cemp.phone AS creator_phone,
        cemp.department_id AS creator_department_id,
        cdep.name AS creator_department,
        cemp.position_id AS creator_position_id,
        cpos.name AS creator_position,
        req.zone AS zone,
        req.break_type AS brake_type,
        req.creator_photo AS creator_photo,
        req.short_description AS short_description,
        req.detailed_description AS detailed_description,
        req.executor_telegram_id AS executor_telegram_id,
        eemp.username AS creator_username,
        eemp.full_name  AS creator_full_name,
        eemp.phone AS creator_phone,
        eemp.department_id AS executor_department_id,
        edep.name AS executor_department,
        eemp.position_id AS executor_position_id,
        epos.name AS executor_position,
        req.executor_photo AS executor_photo,
        req.report AS report,
        req.create_date AS create_date
    FROM {Tables.SCHEMA}.{Tables.REQUEST} AS req
    LEFT JOIN {Tables.SCHEMA}.{Tables.DEPARTMENT} AS dep
    ON req.department_id = dep.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.REQUEST_STATUS} AS rstat
    ON req.status_id = rstat.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.EMPLOYEE} AS cemp
    ON req.creator_telegram_id = cemp.telegram_id
    LEFT JOIN {Tables.SCHEMA}.{Tables.POSITION} AS cpos
    ON cemp.position_id = cpos.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.DEPARTMENT} AS cdep
    ON cemp.department_id = cdep.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.EMPLOYEE} AS eemp
    ON req.executor_telegram_id = eemp.telegram_id
    LEFT JOIN {Tables.SCHEMA}.{Tables.POSITION} AS epos
    ON cemp.position_id = epos.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.DEPARTMENT} AS edep
    ON eemp.department_id = edep.id
    WHERE req.department_id = %(department_id)s
    ORDER BY req.create_date;
'''
SELECT_DEPARTMENT_REQUESTS_BY_STATUS = f'''
    SELECT
        req.bitrix_deal_id AS bitrix_deal_id,
        req.department_id AS department_id,
        dep.name AS department_name,
        req.status_id AS status_id,
        rstat.name AS status_name,
        req.creator_telegram_id AS creator_telegram_id,
        cemp.username AS creator_username,
        cemp.full_name  AS creator_full_name,
        cemp.phone AS creator_phone,
        cemp.department_id AS creator_department_id,
        cdep.name AS creator_department,
        cemp.position_id AS creator_position_id,
        cpos.name AS creator_position,
        req.zone AS zone,
        req.break_type AS brake_type,
        req.creator_photo AS creator_photo,
        req.short_description AS short_description,
        req.detailed_description AS detailed_description,
        req.executor_telegram_id AS executor_telegram_id,
        eemp.username AS creator_username,
        eemp.full_name  AS creator_full_name,
        eemp.phone AS creator_phone,
        eemp.department_id AS executor_department_id,
        edep.name AS executor_department,
        eemp.position_id AS executor_position_id,
        epos.name AS executor_position,
        req.executor_photo AS executor_photo,
        req.report AS report,
        req.create_date AS create_date
    FROM {Tables.SCHEMA}.{Tables.REQUEST} AS req
    LEFT JOIN {Tables.SCHEMA}.{Tables.DEPARTMENT} AS dep
    ON req.department_id = dep.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.REQUEST_STATUS} AS rstat
    ON req.status_id = rstat.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.EMPLOYEE} AS cemp
    ON req.creator_telegram_id = cemp.telegram_id
    LEFT JOIN {Tables.SCHEMA}.{Tables.POSITION} AS cpos
    ON cemp.position_id = cpos.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.DEPARTMENT} AS cdep
    ON cemp.department_id = cdep.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.EMPLOYEE} AS eemp
    ON req.executor_telegram_id = eemp.telegram_id
    LEFT JOIN {Tables.SCHEMA}.{Tables.POSITION} AS epos
    ON cemp.position_id = epos.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.DEPARTMENT} AS edep
    ON eemp.department_id = edep.id
    WHERE req.department_id = %(department_id)s
    AND req.status_id < %(status_id)s
    ORDER BY req.create_date;
'''
SELECT_CURRENT_REQUEST_OF_DEPARTMENT = f'''
    SELECT
        req.bitrix_deal_id AS bitrix_deal_id,
        req.department_id AS department_id,
        dep.name AS department_name,
        req.status_id AS status_id,
        rstat.name AS status_name,
        req.creator_telegram_id AS creator_telegram_id,
        cemp.username AS creator_username,
        cemp.full_name  AS creator_full_name,
        cemp.phone AS creator_phone,
        cemp.department_id AS creator_department_id,
        cdep.name AS creator_department,
        cemp.position_id AS creator_position_id,
        cpos.name AS creator_position,
        req.zone AS zone,
        req.break_type AS brake_type,
        req.creator_photo AS creator_photo,
        req.short_description AS short_description,
        req.detailed_description AS detailed_description,
        req.executor_telegram_id AS executor_telegram_id,
        eemp.username AS creator_username,
        eemp.full_name  AS creator_full_name,
        eemp.phone AS creator_phone,
        eemp.department_id AS executor_department_id,
        edep.name AS executor_department,
        eemp.position_id AS executor_position_id,
        epos.name AS executor_position,
        req.executor_photo AS executor_photo,
        req.report AS report,
        req.create_date AS create_date,
        cemp.last_name AS creator_last_name,
        cemp.first_name AS creator_first_name,
        eemp.last_name AS executor_last_name,
        eemp.first_name AS executor_first_name
    FROM {Tables.SCHEMA}.{Tables.REQUEST} AS req
    LEFT JOIN {Tables.SCHEMA}.{Tables.DEPARTMENT} AS dep
    ON req.department_id = dep.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.REQUEST_STATUS} AS rstat
    ON req.status_id = rstat.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.EMPLOYEE} AS cemp
    ON req.creator_telegram_id = cemp.telegram_id
    LEFT JOIN {Tables.SCHEMA}.{Tables.POSITION} AS cpos
    ON cemp.position_id = cpos.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.DEPARTMENT} AS cdep
    ON cemp.department_id = cdep.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.EMPLOYEE} AS eemp
    ON req.executor_telegram_id = eemp.telegram_id
    LEFT JOIN {Tables.SCHEMA}.{Tables.POSITION} AS epos
    ON cemp.position_id = epos.id
    LEFT JOIN {Tables.SCHEMA}.{Tables.DEPARTMENT} AS edep
    ON eemp.department_id = edep.id
    WHERE req.department_id = %(department_id)s
    AND req.bitrix_deal_id = %(bitrix_deal_id)s
    ORDER BY req.create_date;
'''
SELECT_ANY_ACTIVE_REQUEST_LIST = f'''
    SELECT
        bitrix_deal_id,
        department_id,
        short_description
    FROM {Tables.SCHEMA}.{Tables.REQUEST}
    WHERE status_id < 5
    ORDER BY create_date;
'''
SELECT_DEPARTMENT_ACTIVE_REQUEST_LIST = f'''
    SELECT
        bitrix_deal_id,
        department_id,
        short_description
    FROM {Tables.SCHEMA}.{Tables.REQUEST}
    WHERE status_id < 5 AND department_id = %(department_id)s
    ORDER BY create_date;
'''
SELECT_CREATOR_ANY_ACTIVE_REQUEST_LIST = f'''
    SELECT
        bitrix_deal_id,
        department_id,
        short_description
    FROM {Tables.SCHEMA}.{Tables.REQUEST}
    WHERE status_id < 5 AND creator_telegram_id = %(creator_telegram_id)s
    ORDER BY create_date;
'''
SELECT_CREATOR_DEPARTMENT_ACTIVE_REQUEST_LIST = f'''
    SELECT
        bitrix_deal_id,
        department_id,
        short_description
    FROM {Tables.SCHEMA}.{Tables.REQUEST}
    WHERE status_id < 5 AND creator_telegram_id = %(creator_telegram_id)s
    AND department_id = %(department_id)s
    ORDER BY create_date;
'''
SELECT_EXECUTOR_ANY_ACTIVE_REQUEST_LIST = f'''
    SELECT
        bitrix_deal_id,
        department_id,
        short_description
    FROM {Tables.SCHEMA}.{Tables.REQUEST}
    WHERE status_id < 5 AND department_id = %(department_id)s
    ORDER BY create_date;
'''
SELECT_EXECUTOR_OWN_ACTIVE_REQUEST_LIST = f'''
    SELECT
        bitrix_deal_id,
        department_id,
        short_description
    FROM {Tables.SCHEMA}.{Tables.REQUEST}
    WHERE status_id < 5 AND executor_telegram_id = %(executor_telegram_id)s
    AND department_id = %(department_id)s
    ORDER BY create_date;
'''
SELECT_STATISTIC_OF_DEPARTMENTS = f'''
    WITH new AS (
        SELECT
            department_id,
            COUNT(status_id)
        FROM {Tables.SCHEMA}.{Tables.REQUEST}
        WHERE status_id = 1
        GROUP BY department_id
        ),
        tech_work AS (
        SELECT
            department_id,
            COUNT(status_id)
        FROM {Tables.SCHEMA}.{Tables.REQUEST}
        WHERE status_id = 2
        GROUP BY department_id
        ),
        mgrtech_work AS (
        SELECT
            department_id,
            COUNT(status_id)
        FROM {Tables.SCHEMA}.{Tables.REQUEST}
        WHERE status_id = 3
        GROUP BY department_id
        ),
        headtech_work AS (
        SELECT
            department_id,
            COUNT(status_id)
        FROM {Tables.SCHEMA}.{Tables.REQUEST}
        WHERE status_id = 4
        GROUP BY department_id
        ),
        done AS (
        SELECT
            department_id,
            COUNT(status_id)
        FROM {Tables.SCHEMA}.{Tables.REQUEST}
        WHERE status_id = 5
        GROUP BY department_id
        )
    SELECT
        dep.id,
        dep.name,
        new.count,
        techw.count,
        mgr.count,
        head.count,
        done.count
    FROM {Tables.SCHEMA}.{Tables.DEPARTMENT} AS dep
    LEFT JOIN new AS new ON new.department_id = dep.id
    LEFT JOIN tech_work AS techw ON techw.department_id = dep.id
    LEFT JOIN mgrtech_work AS mgr ON mgr.department_id = dep.id
    LEFT JOIN headtech_work AS head ON head.department_id = dep.id
    LEFT JOIN done AS done ON done.department_id = dep.id
'''
