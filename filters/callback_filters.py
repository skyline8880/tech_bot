from aiogram.filters.callback_data import CallbackData

""" from typing import Optional """

from constants.buttons_init import (ActionButtons, CreatorButtons,
                                    CurrentRequestActionButtons, DateReports,
                                    DepartmentFloor, ExecutorButtons,
                                    ReportsRequest, RequestButtons)
from constants.database_init import Position


class UserActionsCallbackData(CallbackData, prefix='action_is'):
    action: ActionButtons


class UserCreatorCallbackData(CallbackData, prefix='creator_is'):
    creator: CreatorButtons


class UserExecutorCallbackData(CallbackData, prefix='executor_is'):
    executor: ExecutorButtons


class RequestActionCallbackData(CallbackData, prefix='request_is'):
    request: RequestButtons


class DepartmentCallbackData(CallbackData, prefix='department_is'):
    department: str


class PositionCallbackData(CallbackData, prefix='position_is'):
    position: Position


class ZoneCallbackData(CallbackData, prefix='zone_is'):
    zone: str


class BreakTypeCallbackData(CallbackData, prefix='bt_is'):
    break_type: str


class CurrentRequestActionCallbackData(CallbackData, prefix='req_act'):
    current_act: CurrentRequestActionButtons
    status_id: int
    department_id: int
    cur_act_deal: int


class GetCurrentRequestCallbackData(CallbackData, prefix='current_request'):
    request_id: int
    department_id: int


class RequestNavigationCallbackData(CallbackData, prefix='move_to_page'):
    move: str
    page: int


class RequestPageInfoCallbackData(CallbackData, prefix='page_is'):
    page: int


class FloorCallbackData(CallbackData, prefix='floor_is'):
    floor: DepartmentFloor


class ReportsRequestCD(CallbackData, prefix='report_req'):
    report_req: ReportsRequest


class DateReportsCD(CallbackData, prefix='dt_rep'):
    dt_rep: DateReports
