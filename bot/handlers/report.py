from cProfile import label
from http import client
import os
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
from Data.db import get_session

from keyboards.inline import kb_change_market_place, brand_inline, years_inline, month_inline

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
            tg_user = f'@{message.from_user.username}'
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
async def change_brand(callback: CallbackQuery, state: FSMContext):
    if not await is_admin(callback.from_user.id):
        await callback.answer("У вас нет доступа к этой функции.")
        return

    await state.update_data(mp=callback.data)
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
    years = dt['years'].split('_')[1]
    month = dt['month'].split('_')[1]
    mp = dt['mp']
    date = f'{years}-{month}'
    await callback.message.answer('Ожидайте ⌛️')
    
    if mp == 'mp_ozon':
        async with get_session() as session:  # Используем async with для асинхронной сессии
            try:
                tg_user = f'@{callback.from_user.username}'
                print(tg_user)
                res1 = await session.execute(select(Profile.ozon_token).where(Profile.tg_username == tg_user))
                res2 = await session.execute(select(Profile.ozon_client_id).where(Profile.tg_username == tg_user))
                api_key = res1.scalar()
                client_id = res2.scalar()
                
                try:
                    report(api_key=str(api_key), client_id=str(client_id), month=int(month), year=int(years))
                except Exception as ex:
                    print(ex)
                await asyncio.sleep(2)
                file_path = os.path.join('parser', 'reports', 'ozon', f'ozon_{month}_{years}.xlsx')
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
        pprint('Скоро будет')
        # await bot.send_document(chat_id=callback.from_user.id, document=open(f"parser/reports/wb/sales_report.xlsx", 'rb'))
        if brand == 'sec_of_chameleon':
            label = 'Секреты Хамелеона'
            try:
                all_sales(sales_year=years, sales_month=month, label=label, brand=brand, date=date)
                file_path = f'parser/reports/wb/aqua/wb_{brand}_{date}.xlsx'
                if os.path.exists(file_path):
                    pprint('GOOD')
                    with open(file_path, 'rb') as file:
                        document = BufferedInputFile(file.read(), filename=f'wb_{brand}_{date}.xlsx')
                        await bot.send_document(chat_id=callback.from_user.id, document=document)
            except Exception as ex:
                logger.error(f'Ошибка: {ex}')
                await callback.message.answer('По каким-то причинам бот не может сформировать отчет.')
                await callback.answer()
        elif brand == 'cscgaming':
            label = 'CSC Gaming'
            try:
                all_sales(label=label, sales_year=years, sales_month=month, brand=brand, date=date)
                file_path = f'parser/reports/wb/csc/wb_{brand}_{date}.xlsx'
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as file:
                        document = BufferedInputFile(file.read(), filename=f'wb_{brand}_{date}.xlsx')
                        await bot.send_document(chat_id=callback.from_user.id, document=document)
                        await callback.answer()
            except Exception as ex:
                logger.error(f'Ошибка: {ex}')
                await callback.message.answer('По каким-то причинам бот не может сформировать отчет.')
                await callback.answer()
