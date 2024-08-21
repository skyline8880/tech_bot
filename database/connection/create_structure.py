from constants.database_tables import Tables

CREATE_STRUCTURE = f'''
    CREATE SCHEMA IF NOT EXISTS {Tables.SCHEMA};

    CREATE TABLE IF NOT EXISTS {Tables.SCHEMA}.{Tables.DEPARTMENT} (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL UNIQUE,
        bitrix_webhook VARCHAR(250) NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS {Tables.SCHEMA}.{Tables.REQUEST_STATUS} (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS {Tables.SCHEMA}.{Tables.POSITION} (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS {Tables.SCHEMA}.{Tables.BITRIX_ACCOUNT} (
        id SERIAL PRIMARY KEY,
        department_id INTEGER UNIQUE NOT NULL,
        tech BIGINT NOT NULL,
        mgr_tech BIGINT NOT NULL,
        head_tech BIGINT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS {Tables.SCHEMA}.{Tables.EMPLOYEE} (
        id SERIAL PRIMARY KEY,
        is_active BOOLEAN NOT NULL DEFAULT FALSE,
        telegram_id BIGINT,
        username VARCHAR(250),
        full_name VARCHAR(250),
        last_name VARCHAR(250),
        first_name VARCHAR(250),
        position_id INTEGER,
        department_id INTEGER,
        phone VARCHAR(15) NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS {Tables.SCHEMA}.{Tables.REQUEST} (
        id SERIAL PRIMARY KEY,
        bitrix_deal_id BIGINT NOT NULL,
        department_id INTEGER NOT NULL,
        status_id INTEGER NOT NULL,
        creator_telegram_id BIGINT NOT NULL,
        zone VARCHAR(150) NOT NULL,
        break_type VARCHAR(150) NOT NULL,
        creator_photo VARCHAR(500) NOT NULL,
        short_description VARCHAR(150) NOT NULL,
        detailed_description VARCHAR(400) NOT NULL,
        executor_telegram_id BIGINT,
        executor_photo VARCHAR(500),
        report VARCHAR(500),
        create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS {Tables.SCHEMA}.{Tables.BITRIX_FIELD} (
        id SERIAL PRIMARY KEY,
        department_id INTEGER UNIQUE NOT NULL,
        zone VARCHAR(150),
        break_type VARCHAR(150),
        photo VARCHAR(150),
        short_description VARCHAR(150),
        detailed_description VARCHAR(150),
        report VARCHAR(150)
    );

    CREATE TABLE IF NOT EXISTS {Tables.SCHEMA}.{Tables.BITRIX_STAGE} (
        id SERIAL PRIMARY KEY,
        department_id INTEGER UNIQUE NOT NULL,
        category_id BIGINT NOT NULL,
        new VARCHAR(150),
        onmgr VARCHAR(150),
        hangon VARCHAR(150),
        done VARCHAR(150)
    );
'''
