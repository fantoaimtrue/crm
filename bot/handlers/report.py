from cProfile import label
import os
from logger_config import logger
from aiogram import Router, flags, F
from aiogram.types import ChatMember, Message, CallbackQuery, BufferedInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from pprint import pprint
from parser.ozon import report
from parser.wb import all_sales
from main import bot
from config.set import admins

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
    session = get_session()
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
            await message.answer("Выберите маркетплейс 🛍", reply_markup=kb_change_market_place().as_markup())
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")
    finally:
        await session.close()
    


@router.callback_query(F.data.startswith('mp_'))
async def change_brand(callback: CallbackQuery, state: FSMContext):
    if not await is_admin(callback.from_user.id):
        await callback.answer("У вас нет доступа к этой функции.")
        return

    await state.update_data(mp=callback.data)
    await callback.message.edit_text(text='Выберите бренд 💼', reply_markup=brand_inline().as_markup())
    await callback.answer()

@router.callback_query(F.data.startswith('back_brand'))
async def back_brand(callback: CallbackQuery):
    if not await is_admin(callback.from_user.id):
        await callback.answer("У вас нет доступа к этой функции.")
        return

    await callback.message.edit_text('Выберите маркетплейс 🛍', reply_markup=kb_change_market_place().as_markup())
    await callback.answer()

@router.callback_query(F.data.startswith('brand_'))
async def change_year(callback: CallbackQuery, state: FSMContext):
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

    await callback.message.edit_text(text='Выберите бренд 💼', reply_markup=brand_inline().as_markup())
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
    pprint(dt)
    years = dt['years'].split('_')[1]
    month = dt['month'].split('_')[1]
    mp = dt['mp']
    brand = dt['brand'].split('brand_')[1]
    logger.info(f'{brand}')
    date = f'{years}-{month}'
    await callback.message.answer('Ожидайте ⌛️')
    if mp == 'mp_ozon':
        if brand == 'sec_of_chameleon':
            try:
                report(date=date, config=brand)
                file_path = f'parser/reports/ozon/aqua/ozon_{brand}_{date}.xlsx'
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as file:
                        document = BufferedInputFile(file.read(), filename=f'ozon_{brand}_{date}.xlsx')
                        await bot.send_document(chat_id=callback.from_user.id, document=document)
                else:
                    await callback.message.answer('Файл отчета не найден.')
                    logger.info('Файл не найден')
            except Exception as ex:
                pprint(ex)
                await callback.message.answer('По каким-то причинам бот не может сформировать отчет.')
                logger.info(f'По каким-то причинам бот не может сформировать отчет. CODE ERROR : {ex}')

        elif brand == 'cscgaming':
            try:
                report(date=date, config=brand)
                file_path = f'parser/reports/ozon/csc/ozon_{brand}_{date}.xlsx'
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as file:
                        document = BufferedInputFile(file.read(), filename=f'ozon_{brand}_{date}.xlsx')
                        await bot.send_document(chat_id=callback.from_user.id, document=document)
                else:
                    await callback.message.answer('Файл отчета не найден.')
                    logger.info('Файл не найден')
            except Exception as ex:
                pprint(ex)
                await callback.message.answer('По каким-то причинам бот не может сформировать отчет.')
                logger.info(f'По каким-то причинам бот не может сформировать отчет. CODE ERROR : {ex}')

    if mp == 'mp_wildberries':
        pprint('Скоро будет')
        # await bot.send_document(chat_id=callback.from_user.id, document=open(f"parser/reports/wb/sales_report.xlsx", 'rb'))
        if brand == 'sec_of_chameleon':
            label = 'Секреты Хамелеона'
            try:
                all_sales(sales_year=years, sales_month=month, label=label, brand=brand, date=date)
                file_path = f'parser/reports/wb/aqua/wb_{brand}_{date}.xlsx'
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as file:
                        document = BufferedInputFile(file.read(), filename=f'wb_{brand}_{date}.xlsx')
                        await bot.send_document(chat_id=callback.from_user.id, document=document)
                        await callback.answer()
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
