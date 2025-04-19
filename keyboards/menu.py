from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# from bitrix_api.bitrix_api import BitrixMethods
from constants.buttons_init import (ActionButtons, CreatorButtons,
                                    CurrentRequestActionButtons, DateReports,
                                    ReportsRequest, RequestButtons)
from constants.database_init import Department, Position
from filters.callback_filters import (CurrentRequestActionCallbackData,
                                      DateReportsCD, DepartmentCallbackData,
                                      # FloorCallbackData,
                                      GetCurrentRequestCallbackData,
                                      PositionCallbackData, ReportsRequestCD,
                                      RequestActionCallbackData,
                                      RequestNavigationCallbackData,
                                      RequestPageInfoCallbackData,
                                      UserActionsCallbackData,
                                      UserCreatorCallbackData)

cancel_button = [
    InlineKeyboardButton(
        text=ActionButtons.CANCEL.value,
        callback_data=UserActionsCallbackData(
            action=ActionButtons.CANCEL).pack())
]
cancel_keyboard = InlineKeyboardMarkup(
    row_width=1, inline_keyboard=[cancel_button])

menu_button = [
    InlineKeyboardButton(
        text=ActionButtons.MENU.value,
        callback_data=UserActionsCallbackData(
            action=ActionButtons.MENU).pack())
]
menu_keyboard = InlineKeyboardMarkup(
    row_width=1, inline_keyboard=[menu_button])

back_button = [
    InlineKeyboardButton(
        text=ActionButtons.BACK.value,
        callback_data=UserActionsCallbackData(
            action=ActionButtons.BACK).pack())
]
back_keyboard = InlineKeyboardMarkup(
    row_width=1, inline_keyboard=[back_button])


""" def create_menu_by_position(position_id):
    if position_id < 6:
        menu_buttons = []
        empl_work = []
        creator_button_low_border = 0
        for num, button in enumerate(CreatorButtons, start=1):
            if position_id == 5:
                creator_button_low_border = 2
            if creator_button_low_border < num and num < 4:
                empl_work.append(
                    InlineKeyboardButton(
                        text=button.value,
                        callback_data=UserCreatorCallbackData(
                            creator=button).pack())
                )
            if num >= 4:
                if empl_work != []:
                    menu_buttons.append(empl_work)
                    empl_work = []
                menu_buttons.append(
                    [
                        InlineKeyboardButton(
                            text=button.value,
                            callback_data=UserCreatorCallbackData(
                                creator=button).pack())
                    ]
                )
        return InlineKeyboardMarkup(
            row_width=2, inline_keyboard=menu_buttons)
    menu_buttons = []
    for num, button in enumerate(RequestButtons, start=1):
        if num > 1 and num < 4:
            menu_buttons.append(
                [
                    InlineKeyboardButton(
                        text=button.value,
                        callback_data=RequestActionCallbackData(
                            request=button).pack())
                ]
            )
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=menu_buttons) """


def create_menu_by_position(position_id):
    creator_menu_borders = [0, 6]
    request_menu_borders = [5, 6]
    if not int(position_id) < 5:
        creator_menu_borders = [6, 7]
        request_menu_borders = [0, 5]
        if not int(position_id) < 6:
            request_menu_borders = [1, 4]
    menu_buttons = []
    hire_fire = []
    for num, button in enumerate(CreatorButtons, start=1):
        if creator_menu_borders[0] < num and num < creator_menu_borders[1]:
            if num < 3:
                hire_fire.append(
                    InlineKeyboardButton(
                        text=button.value,
                        callback_data=UserCreatorCallbackData(
                            creator=button).pack())
                )
            else:
                if len(hire_fire) != []:
                    menu_buttons.append(hire_fire)
                    hire_fire = []
                menu_buttons.append(
                    [
                        InlineKeyboardButton(
                            text=button.value,
                            callback_data=UserCreatorCallbackData(
                                creator=button).pack())
                    ]
                )
    for num, button in enumerate(RequestButtons, start=1):
        if request_menu_borders[0] < num and num < request_menu_borders[1]:
            menu_buttons.append(
                [
                    InlineKeyboardButton(
                        text=button.value,
                        callback_data=RequestActionCallbackData(
                            request=button).pack())
                ]
            )
    return InlineKeyboardMarkup(
        row_width=2, inline_keyboard=menu_buttons)


def create_request_menu():
    request_buttons = []
    for button in RequestButtons:
        request_buttons.append(
            [
                InlineKeyboardButton(
                    text=button.value,
                    callback_data=RequestActionCallbackData(
                        request=button).pack())
            ]
        )
    request_buttons.append(menu_button)
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=request_buttons)


def create_departments_menu(position_id, department_id):
    menu_buttons = []
    depart_menu_borders = [int(department_id - 1), int(department_id) + 1]
    if int(position_id) < 4:
        depart_menu_borders = [1, 6]
    for num, button in enumerate(Department, start=1):
        if depart_menu_borders[0] < num and num < depart_menu_borders[1]:
            menu_buttons.append(
                [
                    InlineKeyboardButton(
                        text=button.value[0],
                        callback_data=DepartmentCallbackData(
                            department=button.value[0]).pack())
                ]
            )
    menu_buttons.append(cancel_button)
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=menu_buttons)


def create_positions_menu(position_id):
    menu_buttons = []
    for num, button in enumerate(Position, start=1):
        if position_id < num:
            menu_buttons.append(
                [
                    InlineKeyboardButton(
                        text=button.value,
                        callback_data=PositionCallbackData(
                            position=button.value).pack())
                ]
            )
    menu_buttons.append(cancel_button)
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=menu_buttons)


""" async def create_floor_menu(floor_data):
    menu_buttons = []
    btn_row = []
    for name in floor_data.keys():
        btn_row.append(
            InlineKeyboardButton(
                text=f'{name}',
                callback_data=FloorCallbackData(
                    floor=f'{name}').pack()))
        if len(btn_row) == 2:
            menu_buttons.append(btn_row)
            btn_row = []
    if btn_row != []:
        menu_buttons.append(btn_row)
    menu_buttons.append(back_button)
    return InlineKeyboardMarkup(
        row_width=2, inline_keyboard=menu_buttons) """


"""async def create_zone_menu(department_id, floor=None):
    menu_buttons = []
    btn_row = []
    if floor is None:
        bm = await BitrixMethods(
            department_sign=department_id).collect_portal_data()
        zone_data = await bm.get_zone_key_value()
        for name in zone_data.keys():
            btn_row.append(
                InlineKeyboardButton(
                    text=f'🧾 {name}',
                    callback_data=ZoneCallbackData(
                        zone=f'🧾 {name}').pack()))
            if len(btn_row) == 2:
                menu_buttons.append(btn_row)
                btn_row = []
        if btn_row != []:
            menu_buttons.append(btn_row)
        menu_buttons.append(back_button)
        return InlineKeyboardMarkup(
            row_width=2, inline_keyboard=menu_buttons)
    zone_data = await CreateZoneKeyboard(
        department_id).get_floor_area_dict(floor=floor)
    for name in zone_data.keys():
        btn_row.append(
            InlineKeyboardButton(
                text=f'🧾 {name}',
                callback_data=ZoneCallbackData(
                    zone=f'🧾 {name}').pack()))
        if len(btn_row) == 2:
            menu_buttons.append(btn_row)
            btn_row = []
    if btn_row != []:
        menu_buttons.append(btn_row)
    menu_buttons.append(back_button)
    return InlineKeyboardMarkup(
        row_width=2, inline_keyboard=menu_buttons)


async def create_break_type_menu(department_id):
    bm = await BitrixMethods(
        department_sign=department_id).collect_portal_data()
    break_type_data = await bm.get_break_type_key_value()
    menu_buttons = []
    btn_row = []
    for name in break_type_data.keys():
        btn_row.append(
            InlineKeyboardButton(
                text=f'🔧 {name}',
                callback_data=BreakTypeCallbackData(
                    break_type=f'🔧 {name}').pack()))
        if len(btn_row) == 2:
            menu_buttons.append(btn_row)
            btn_row = []
    if btn_row != []:
        menu_buttons.append(btn_row)
    menu_buttons.append(back_button)
    return InlineKeyboardMarkup(
        row_width=2, inline_keyboard=menu_buttons)"""


""" def create_current_request_menu(
        position_id, request_status_id, is_creator, is_executor):
    if position_id == 6:
        if request_status_id == 1:
            menu_buttons = [
                [
                    InlineKeyboardButton(
                        text=CurrentRequestActionButtons.INROLE.value,
                        callback_data=CurrentRequestActionCallbackData(
                            current_act=CurrentRequestActionButtons.INROLE
                                ).pack())
                ]
            ]
            menu_buttons.append(menu_button)
            return InlineKeyboardMarkup(
                row_width=1, inline_keyboard=menu_buttons)
        elif request_status_id == 2:
            menu_buttons = []
            if not is_executor:
                menu_buttons = [
                    [
                        InlineKeyboardButton(
                            text=CurrentRequestActionButtons.INROLE.value,
                            callback_data=CurrentRequestActionCallbackData(
                                current_act=CurrentRequestActionButtons.INROLE
                                    ).pack())
                    ]
                ]
                menu_buttons.append(menu_button)
                return InlineKeyboardMarkup(
                    row_width=1, inline_keyboard=menu_buttons)
            menu_buttons.append(
                [
                    InlineKeyboardButton(
                        text=CurrentRequestActionButtons.HANDOVERMGR.value,
                        callback_data=CurrentRequestActionCallbackData(
                            current_act=CurrentRequestActionButtons.HANDOVERMGR
                                ).pack())
                ],
            )
            menu_buttons.append(
                [
                    InlineKeyboardButton(
                        text=CurrentRequestActionButtons.DONE.value,
                        callback_data=CurrentRequestActionCallbackData(
                            current_act=CurrentRequestActionButtons.DONE
                                ).pack())
                ],
            )
            # menu_buttons.append(menu_button)
            return InlineKeyboardMarkup(
                row_width=1, inline_keyboard=menu_buttons)
        menu_buttons = [
            [
                InlineKeyboardButton(
                    text=CurrentRequestActionButtons.DONE.value,
                    callback_data=CurrentRequestActionCallbackData(
                        current_act=CurrentRequestActionButtons.DONE
                            ).pack())
            ],
        ]
        menu_buttons.append(menu_button)
        return InlineKeyboardMarkup(
            row_width=1, inline_keyboard=menu_buttons)
    menu_buttons = [
        [
            InlineKeyboardButton(
                text=CurrentRequestActionButtons.HANDOVERMGR.value,
                callback_data=CurrentRequestActionCallbackData(
                    current_act=CurrentRequestActionButtons.HANDOVERMGR
                        ).pack())
        ],
        [
            InlineKeyboardButton(
                text=CurrentRequestActionButtons.HANGON.value,
                callback_data=CurrentRequestActionCallbackData(
                    current_act=CurrentRequestActionButtons.HANGON
                        ).pack())
        ],
        [
            InlineKeyboardButton(
                text=CurrentRequestActionButtons.DONE.value,
                callback_data=CurrentRequestActionCallbackData(
                    current_act=CurrentRequestActionButtons.DONE
                        ).pack())
        ],
    ]
    menu_buttons.append(back_button)
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=menu_buttons) """


def create_current_request_menu(user_data, current_deal):
    (
        bitrix_deal_id,
        deal_department_id,
        department_name,
        status_id,
        status_name,
        creator_telegram_id,
        creator_username,
        creator_full_name,
        creator_phone,
        creator_department_id,
        creator_department,
        creator_position_id,
        creator_position,
        creator_photo,
        short_description,
        detailed_description,
        executor_telegram_id,
        creator_username,
        creator_full_name,
        creator_phone,
        executor_department_id,
        executor_department,
        executor_position_id,
        executor_position,
        executor_photo,
        report,
        create_date,
        creator_last_name,
        creator_first_name,
        executor_last_name,
        executor_first_name) = current_deal
    (
        is_active,
        telegram_id,
        username,
        full_name,
        position_id,
        name,
        department_id,
        name,
        phone,
        last_name,
        first_name
    ) = user_data
    fbutton = CurrentRequestActionButtons.INROLE
    second_row_buttons = []
    if 1 < status_id and status_id < 4:
        fbutton = CurrentRequestActionButtons.DONE
        second_row_buttons = [
            InlineKeyboardButton(
                text=CurrentRequestActionButtons.HANDOVERMGR.value,
                callback_data=CurrentRequestActionCallbackData(
                    current_act=CurrentRequestActionButtons.HANDOVERMGR,
                    status_id=status_id,
                    ##creator_id=creator_telegram_id,
                    ##executor_id=executor_telegram_id,
                    department_id=deal_department_id,
                    cur_act_deal=bitrix_deal_id
                        ).pack()),
            InlineKeyboardButton(
                text=CurrentRequestActionButtons.HANGON.value,
                callback_data=CurrentRequestActionCallbackData(
                    current_act=CurrentRequestActionButtons.HANGON,
                    status_id=status_id,
                    #creator_id=creator_telegram_id,
                    #executor_id=executor_telegram_id,
                    department_id=deal_department_id,
                    cur_act_deal=bitrix_deal_id
                        ).pack()),
        ]
    first_row_button = [
        InlineKeyboardButton(
            text=fbutton.value,
            callback_data=CurrentRequestActionCallbackData(
                current_act=fbutton,
                status_id=status_id,
                #creator_id=creator_telegram_id,
                #executor_id=executor_telegram_id,
                department_id=deal_department_id,
                cur_act_deal=bitrix_deal_id
                    ).pack()),
    ]
    kbrd = [first_row_button]
    if second_row_buttons != []:
        kbrd.append(second_row_buttons)


    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=kbrd)
    """ elif request_status_id == 2:
        menu_buttons = []
        if not is_executor:
            menu_buttons = [
                [
                    InlineKeyboardButton(
                        text=CurrentRequestActionButtons.INROLE.value,
                        callback_data=CurrentRequestActionCallbackData(
                            current_act=CurrentRequestActionButtons.INROLE
                                ).pack())
                ]
            ]
            menu_buttons.append(menu_button)
            return InlineKeyboardMarkup(
                row_width=1, inline_keyboard=menu_buttons)
        menu_buttons.append(
            [
                InlineKeyboardButton(
                    text=CurrentRequestActionButtons.HANDOVERMGR.value,
                    callback_data=CurrentRequestActionCallbackData(
                        current_act=CurrentRequestActionButtons.HANDOVERMGR
                            ).pack())
            ],
        )
        menu_buttons.append(
            [
                InlineKeyboardButton(
                    text=CurrentRequestActionButtons.DONE.value,
                    callback_data=CurrentRequestActionCallbackData(
                        current_act=CurrentRequestActionButtons.DONE
                            ).pack())
            ],
        )
        menu_buttons.append(menu_button)
        return InlineKeyboardMarkup(
            row_width=1, inline_keyboard=menu_buttons)
    menu_buttons = [
        [
            InlineKeyboardButton(
                text=CurrentRequestActionButtons.DONE.value,
                callback_data=CurrentRequestActionCallbackData(
                    current_act=CurrentRequestActionButtons.DONE
                        ).pack())
        ],
    ]
    menu_buttons.append(menu_button)
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=menu_buttons)
menu_buttons = [
    [
        InlineKeyboardButton(
            text=CurrentRequestActionButtons.HANDOVERMGR.value,
            callback_data=CurrentRequestActionCallbackData(
                current_act=CurrentRequestActionButtons.HANDOVERMGR
                    ).pack())
    ],
    [
        InlineKeyboardButton(
            text=CurrentRequestActionButtons.HANGON.value,
            callback_data=CurrentRequestActionCallbackData(
                current_act=CurrentRequestActionButtons.HANGON
                    ).pack())
    ],
    [
        InlineKeyboardButton(
            text=CurrentRequestActionButtons.DONE.value,
            callback_data=CurrentRequestActionCallbackData(
                current_act=CurrentRequestActionButtons.DONE
                    ).pack())
    ],
]
menu_buttons.append(back_button)
return InlineKeyboardMarkup(
    row_width=1, inline_keyboard=menu_buttons) """


def navigation(page, max_pages):
    navigation_buttons = []
    if page == 1 and max_pages == 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                text=f'{page}/{max_pages}',
                callback_data=RequestPageInfoCallbackData(
                    page=page).pack()))
    elif page == 1 and max_pages > 1:
        navigation_buttons.append(InlineKeyboardButton(
            text=f'{page}/{max_pages}',
            callback_data=RequestPageInfoCallbackData(
                page=page).pack()))
        navigation_buttons.append(InlineKeyboardButton(
            text='➡',
            callback_data=RequestNavigationCallbackData(
                move='next', page=page + 1).pack()))
    elif page > 1 and max_pages > page:
        navigation_buttons.append(InlineKeyboardButton(
            text='⬅',
            callback_data=RequestNavigationCallbackData(
                move='previous', page=page - 1).pack()))
        navigation_buttons.append(InlineKeyboardButton(
            text=f'{page}/{max_pages}',
            callback_data=RequestPageInfoCallbackData(
                page=page).pack()))
        navigation_buttons.append(InlineKeyboardButton(
            text='➡',
            callback_data=RequestNavigationCallbackData(
                move='next', page=page + 1).pack()))
    elif page > 1 and max_pages == page:
        navigation_buttons.append(InlineKeyboardButton(
            text='⬅',
            callback_data=RequestNavigationCallbackData(
                move='previous', page=page - 1).pack()))
        navigation_buttons.append(InlineKeyboardButton(
            text=f'{page}/{max_pages}',
            callback_data=RequestPageInfoCallbackData(
                page=page).pack()))
    return navigation_buttons


def create_request_list_menu(page, data, position_id):
    request_count = len(data)
    start = page * 5 - 5
    end = start + 5
    if request_count < end:
        end = request_count + 1
    page_count = request_count // 5
    if request_count // 5 < request_count / 5:
        page_count = request_count // 5 + 1
    request_list_buttons = []
    for request in data[start:end]:
        request_list_buttons.append(
            [
                InlineKeyboardButton(
                    text=f'{request[1]}/{request[0]}: {request[2]}',
                    callback_data=GetCurrentRequestCallbackData(
                        request_id=request[0],
                        department_id=request[1]
                    ).pack()
                )
            ]
        )
    request_list_buttons.append(navigation(page=page, max_pages=page_count))
    if position_id < 4:
        request_list_buttons.append(back_button)
    request_list_buttons.append(menu_button)
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=request_list_buttons)


def current_request_keyboard(department_id, deal_id, title):
    request_button = [
        InlineKeyboardButton(
            text=f'{department_id}/{deal_id}: {title}',
            callback_data=GetCurrentRequestCallbackData(
                request_id=deal_id,
                department_id=department_id
            ).pack()
        )
    ]
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=[request_button])


def reports_keyboard():  # Меню отчетов
    buttons = []

    for butt in ReportsRequest:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=butt.value,
                    callback_data=ReportsRequestCD(report_req=butt).pack()
                )
            ]
        )
    buttons.append(
        [
            InlineKeyboardButton(
                text=ActionButtons.MENU.value,
                callback_data=UserActionsCallbackData(
                    action=ActionButtons.MENU).pack())
        ]
    )
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=buttons)


def date_reports_keyboard():  # Меню выбора периода
    buttons = []

    for butt in DateReports:
        buttons.append([
            InlineKeyboardButton(
                text=butt.value,
                callback_data=DateReportsCD(dt_rep=butt).pack())
            ]
        )
    buttons.append(
        [
            InlineKeyboardButton(
                text=CreatorButtons.REPORT.value,
                callback_data=UserCreatorCallbackData(
                    creator=CreatorButtons.REPORT).pack()
                    )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_reports():
    menu_button = [
        InlineKeyboardButton(
                text=CreatorButtons.REPORT.value,
                callback_data=UserCreatorCallbackData(
                    creator=CreatorButtons.REPORT).pack()
                    )
    ]
    return InlineKeyboardMarkup(
        row_width=2, inline_keyboard=[menu_button])
