from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo


def kb_report():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='/report', callback_data='kb_report')
        ],
    ])
    return ikb


# def kb_web_app():
#     builder = ReplyKeyboardBuilder()
#     builder.add(KeyboardButton(text='Секреты хамелеона', web_app=WebAppInfo(url='https://qna.habr.com/q/1281828')))
#     return builder