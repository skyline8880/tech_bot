import base64
import sys


def create_deal_json(
        title,
        assigned_by,
        category_id,
        stage_id,
        short_description,
        detailed_description,
        break_type,
        zone,
        photo_path,
        short_description_field,
        detailed_description_field,
        break_type_field,
        zone_field,
        photo_field):
    separator = '/'
    if sys.platform == 'win32':
        separator = '\\'
    photo_name = photo_path.split(separator)[-1]
    photo_encode = base64.b64encode(
        open(file=photo_path, mode='rb').read()).decode('utf-8')
    return {
        'fields': {
            'TITLE': title,
            'ASSIGNED_BY_ID': assigned_by,
            'CATEGORY_ID': category_id,
            'STAGE_ID': stage_id,
            f'{short_description_field}': short_description,
            f'{detailed_description_field}': detailed_description,
            f'{break_type_field}': break_type,
            f'{zone_field}': zone,
            f'{photo_field}': {
                'fileData': [
                    photo_name,
                    photo_encode
                ]
            },
        }
    }


def asign_deal_id_on_title(deal_id, title):
    return {
        'ID': deal_id,
        'fields': {
            'TITLE': f'{deal_id}: {title}',
        }
    }


def update_json(deal_id, params):
    return {
        'ID': deal_id,
        'fields': params
    }


def update_on_close_json(
        deal_id,
        stage_id,
        report,
        report_field):
    return {
        'ID': deal_id,
        'fields': {
            'STAGE_ID': stage_id,
            report_field: report,
        }
    }


def timeline_add_on_handover_json(deal_id, comment):
    return {
        'fields': {
            'ENTITY_ID': deal_id,
            'ENTITY_TYPE': 'deal',
            'COMMENT': comment,
        }
    }


def timeline_add_on_close_json(
        deal_id,
        photo_path,
        comment):
    separator = '/'
    if sys.platform == 'win32':
        separator = '\\'
    photo_name = photo_path.split(separator)[-1]
    photo_encode = base64.b64encode(
        open(file=photo_path, mode='rb').read()).decode('utf-8')
    return {
        'fields': {
            'ENTITY_ID': deal_id,
            'ENTITY_TYPE': 'deal',
            'COMMENT': comment,
            'FILES': {'fileData': [photo_name, photo_encode]}
        }
    }


""" def update_on_close_json(
        deal_id,
        photo_path,
        stage_id,
        report,
        photo_field,
        report_field):
    separator = '/'
    if sys.platform == 'win32':
        separator = '\\'
    photo_name = photo_path.split(separator)[-1]
    photo_encode = base64.b64encode(
        open(file=photo_path, mode='rb').read()).decode('utf-8')
    return {
        'ID': deal_id,
        'fields': {
            'STAGE_ID': stage_id,
            report_field: report,
            photo_field: {
                'fileData': [
                    photo_name,
                    photo_encode
                ]
            }
        }
    } """
