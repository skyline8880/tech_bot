from core.secrets import DatabaseSecrets


class Tables:
    SCHEMA = DatabaseSecrets.SCHEMA_NAME
    DEPARTMENT = 'department'
    BITRIX_POSITION = 'bitrix_position'
    POSITION = 'position'
    REQUEST_STATUS = 'request_status'
    BITRIX_ACCOUNT = 'bitrix_account'
    BITRIX_FIELD = 'bitrix_fields'
    BITRIX_STAGE = 'bitrix_stage'
    EMPLOYEE = 'employee'
    REQUEST = 'request'
