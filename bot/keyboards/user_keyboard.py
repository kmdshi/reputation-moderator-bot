from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_ikb() -> InlineKeyboardMarkup:
    '''getting a keyboard to call the report'''
    kb = InlineKeyboardMarkup(row_width=2)
    button_cancel_from_user = InlineKeyboardButton("Отменить репорт", callback_data="cancel_action")
    kb.add(button_cancel_from_user)
    button_cancel_from_admin = InlineKeyboardButton("Отклонить", callback_data="cancel_action_admin")
    button_accept_from_admin = InlineKeyboardButton("Подтвердить", callback_data="accept_action_admin")
    kb.add(button_accept_from_admin, button_cancel_from_admin)
    
    return kb