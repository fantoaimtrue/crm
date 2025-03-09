from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from Data.models import Shops, Profile
from Data.db import get_session
from sqlalchemy.future import select
from decouple import config


def kb_builder():
    builder = InlineKeyboardBuilder()
    for i in range(1, 17):
        builder.row(InlineKeyboardButton(text=str(i), callback_data=str(i)))
        builder.adjust(4, 3)
    return builder


def kb_report():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='/report', callback_data='kb_report')
        ],
    ])
    return ikb


def kb_change_market_place():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Ozon', callback_data='mp_ozon'))
    builder.add(InlineKeyboardButton(text='Wildberries', callback_data='mp_wildberries'))
    builder.adjust(2)
    return builder


async def kb_change_brand(tg_user):
    async with get_session() as session:
        result_1 = await session.execute(
            select(Profile).filter(Profile.tg_username == tg_user)
        )
        username = result_1.scalar_one_or_none()
        user_id = username.user_id
        
        result_2 = await session.execute(
            select(Shops).filter(Shops.user_id == user_id)
        )
        shops = result_2.scalars().all()
        builder = InlineKeyboardBuilder()
        for shop in shops:
            shop_name = shop.shop_name
            builder.add(InlineKeyboardButton(text=f'{shop_name}', callback_data=f'brand_{shop_name}'))
        builder.adjust(2)
        return builder.as_markup()


def brand_inline():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Секреты Хамелеона', callback_data='brand_sec_of_chameleon'))
    builder.add(InlineKeyboardButton(text='CSC GAMING', callback_data='brand_cscgaming'))
    builder.add(InlineKeyboardButton(text='Назад 🔙', callback_data='back_brand'))
    builder.adjust(2)
    return builder


def years_inline():
    builder = InlineKeyboardBuilder()
    for date in range(2024, 2029):
        builder.add(InlineKeyboardButton(text=str(date), callback_data=f'years_{date}'))
    builder.add(InlineKeyboardButton(text='Назад 🔙', callback_data='back_years'))
    builder.adjust(4)
    return builder


all_month = {
    'Январь': '01',
    'Февраль': '02',
    'Март': '03',
    'Апрель': '04',
    'Май': '05',
    'Июнь': '06',
    'Июль': '07',
    'Август': '08',
    'Сентябрь': '09',
    'Октябрь': '10',
    'Ноябрь': '11',
    'Декабрь': '12',
}


def month_inline():
    builder = InlineKeyboardBuilder()
    for month, dt in all_month.items():
        builder.add(InlineKeyboardButton(text=month, callback_data=f'month_{dt}'))
    builder.add(InlineKeyboardButton(text='Назад 🔙', callback_data='back_years'))
    builder.adjust(4)
    return builder


def instruction():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Прочитать инструкцию', url='https://docs.google.com/document/d/1H5lK66Ex7cAaAWNBx5_R26Y9Gv-8EZxAYI3g0ukS8nE/edit?usp=sharing'))
    builder.adjust(1)
    return builder.as_markup()


def webapp():
    url = "https://t.me/helper_ozon_wb_bot/CRMMARKETPLACEHELPER"  # Убедитесь, что это правильный URL
    print(f"Web App URL: {url}") 
    

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Открыть web-панель", web_app=WebAppInfo(url=url)))
    builder.adjust(1)
    return builder.as_markup()

