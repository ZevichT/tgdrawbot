from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_kb(draws):
    buttons = [InlineKeyboardButton(callback_data=f'pc {draw}', text=draw) for draw in draws]
    buttons = [[button] for button in buttons]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
def admin_kb(draws):
    buttons = [InlineKeyboardButton(callback_data=f'end {draw}', text=draw) for draw in draws]
    buttons = [[button] for button in buttons]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard