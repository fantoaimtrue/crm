from cProfile import label
from http import client
import os
from tkinter import NO
from logger_config import logger
from aiogram import Router, flags, F
from aiogram.types import InputFile
from aiogram.types import ChatMember, Message, CallbackQuery, BufferedInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from pprint import pprint
from parser.ozon import report
from parser.wb import all_sales
from main import bot
from config.set import admins
import asyncio


from sqlalchemy.future import select
from Data.models import Profile
from Data.models import Shops
from Data.db import get_session

from keyboards.inline import kb_change_brand, kb_change_market_place, brand_inline, years_inline, month_inline

router = Router()

ADMIN_IDS = admins  # ID администраторов

async def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

async def is_group_admin(chat_id: int, user_id: int) -> bool:
    member = await bot.get_chat_member(chat_id, user_id)
    return member.status in [ChatMember.ADMINISTRATOR, ChatMember.CREATOR]


@router.message(Command(commands=["report"]))
async def cmd_start(message: Message):
    async with get_session() as session:  # Используем async with для асинхронной сессии
        try:
            tg_user = message.from_user.username
            result = await session.execute(select(Profile).where(Profile.tg_username == tg_user))
            profile = result.scalars().first()

            if profile:
                await message.answer("Выберите маркетплейс 🛍", reply_markup=kb_change_market_place().as_markup())
            else:
                await message.answer("Профиль не найден.")
                if not await is_admin(message.from_user.id):
                    await message.answer("У вас нет доступа к этой команде.")
                    return
        except Exception as e:
            await message.answer(f"Произошла ошибка: {str(e)}")

    

@router.callback_query(F.data.startswith('mp_'))
async def change_shop(callback: CallbackQuery, state: FSMContext):
    if not await is_admin(callback.from_user.id):
        await callback.answer("У вас нет доступа к этой функции.")
        return
    user = callback.from_user.username
    await state.update_data(mp=callback.data)
    await callback.message.answer('Выбири магазин', reply_markup=await kb_change_brand(tg_user=user))
    await callback.answer()


@router.callback_query(F.data.startswith('brand_'))
async def change_brand(callback: CallbackQuery, state: FSMContext):
    if not await is_admin(callback.from_user.id):
        await callback.answer("У вас нет доступа к этой функции.")
        return

    await state.update_data(brand=callback.data)
    await callback.message.edit_text(text='Выберите дату отчета', reply_markup=years_inline().as_markup())
    await callback.answer()
    


@router.callback_query(F.data.startswith('back_years'))
async def back_years(callback: CallbackQuery):
    if not await is_admin(callback.from_user.id):
        await callback.answer("У вас нет доступа к этой функции.")
        return

    await callback.message.edit_text("Выберите маркетплейс 🛍", reply_markup=kb_change_market_place().as_markup())
    await callback.answer()

@router.callback_query(F.data.startswith('years_'))
async def change_month(callback: CallbackQuery, state: FSMContext):
    if not await is_admin(callback.from_user.id):
        await callback.answer("У вас нет доступа к этой функции.")
        return

    await callback.message.edit_reply_markup(reply_markup=month_inline().as_markup())
    await state.update_data(years=callback.data)
    await callback.answer()

@router.callback_query(F.data.startswith('back_years'))
async def back_month(callback: CallbackQuery):
    if not await is_admin(callback.from_user.id):
        await callback.answer("У вас нет доступа к этой функции.")
        return

    await callback.message.edit_reply_markup(reply_markup=years_inline())
    await callback.answer()

@router.callback_query(F.data.startswith('month_'))
async def change_finish(callback: CallbackQuery, state: FSMContext):
    if not await is_admin(callback.from_user.id):
        await callback.answer("У вас нет доступа к этой функции.")
        return

    await state.update_data(month=callback.data)
    dt = await state.get_data()

    # Проверяем, что 'years', 'month' и 'mp' существуют в состоянии
    years = dt.get('years', None)
    month = dt.get('month', None)
    mp = dt.get('mp', None)
    brand = dt.get('brand', None)

    if not (years and month and mp and brand):
        await callback.message.answer("Ошибка: данные отчета неполные.")
        return

    years = years.split('_')[1]
    month = month.split('_')[1]
    date = f'{years}-{month}'
    br = brand[brand.index("_") + 1:]
    print(mp)
    await callback.message.answer('Ожидайте ⌛️')
    
    if mp == 'mp_ozon':
        async with get_session() as session:  # Используем async with для асинхронной сессии
            try:
                tg_user = callback.from_user.username
                print(tg_user)
                
                
                
                result_1 = await session.execute(
                    select(Profile).filter(Profile.tg_username == tg_user)
                )
                username = result_1.scalar_one_or_none()
                user_id = username.user_id
                                
                
                res1 = await session.execute(select(Shops.shop_ozon_token).where(Shops.shop_name == br, Shops.user_id == user_id))
                res2 = await session.execute(select(Shops.shop_ozon_client_id).where(Shops.shop_name == br, Shops.user_id == user_id))
                api_key = res1.scalar()
                client_id = res2.scalar()
                
                try:
                    report(api_key=str(api_key), client_id=str(client_id), month=int(month), year=int(years))
                except Exception as ex:
                    print(ex)
                await asyncio.sleep(2)
                file_path = os.path.join('bot', 'parser', 'reports', 'ozon', f'ozon_{month}_{years}.xlsx')
                print(file_path)
                if os.path.exists(file_path):
                    print(f"Файл найден: {file_path}")
                else:
                    print(f"Файл НЕ найден: {file_path}")
                document = FSInputFile(file_path)
                # Отправляем файл пользователю
                await bot.send_document(callback.message.chat.id, document)
            except Exception as e:
                await callback.message.answer(f"Произошла ошибка: {str(e)}")
 
        
        

    if mp == 'mp_wildberries':
        async with get_session() as session:
            try:
                tg_user = callback.from_user.username
                res3 = await session.execute(select(Profile.wb_token).where(Profile.tg_username == tg_user))
                wb_api = res3.scalar()
                if not wb_api:
                    await callback.message.answer("Ошибка: токен Wildberries не найден.")
                    return
                all_sales(api_key=str(wb_api), sales_year=years, sales_month=month, date=date)
                file_path = os.path.join('bot', 'parser', 'reports', 'wb', f'wb_{date}.xlsx')
                print(file_path)
                if os.path.exists(file_path):
                    print(f"Файл найден: {file_path}")
                else:
                    print(f"Файл НЕ найден: {file_path}")
                document = FSInputFile(file_path)
                # Отправляем файл пользователю
                await bot.send_document(callback.message.chat.id, document)
            except Exception as e:
                await callback.message.answer(f"Произошла ошибка: {str(e)}")
        