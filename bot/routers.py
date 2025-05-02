from random import shuffle
from time import sleep

from aiogram import Router, F
from aiogram.filters import Command

from config import admin, bot
from database import DrawsRepository, UsersDrawRepository, UsersRepository
from aiogram.types import CallbackQuery, Message

from .keyboard import main_kb, admin_kb

router = Router()

@router.callback_query(F.data.startswith('pc'))
async def process_draw_callback(callback: CallbackQuery):
    data = callback.data.split()[1]
    await callback.answer()
    draw_id = await DrawsRepository.get_id(data)
    if draw_id == 'Error':
        await bot.send_message(callback.message.chat.id, text='Розыгрыша нет или он удалён')
    else:
        participation = await UsersDrawRepository.check_participation('@'+f'{callback.from_user.username}', draw_id)
        if participation:
            await callback.message.answer('Вы уже участвуете в этом розыгрыше!')
        else:
            await UsersDrawRepository.add_participant(callback.from_user.username, draw_id)
            await callback.message.answer(f'Вы приняли участие в розыгрыше: {data}')


@router.callback_query(F.data.startswith('end'))
async def admin_end_draw(callback: CallbackQuery):
    if callback.from_user.id == admin:
        data = callback.data.split()[1]
        await callback.answer()
        draw_id = await DrawsRepository.get_id(data)
        if draw_id == 'Error':
            await bot.send_message(callback.message.chat.id, text='Розыгрыша нет или он удалён')
        else:
            users_id = await UsersDrawRepository.get_users_id(draw_id)
            participants = [userid for userid in users_id]
            winners_count = await DrawsRepository.get_max_winners(draw_id)
            if winners_count == 'Error':
                await bot.send_message(callback.message.chat.id, text='Ошибка. Количество победителей не получено')
            else:
                if len(participants) < winners_count + 1:
                    await callback.message.answer(f'Недостаточно участников: {len(participants)}. Необходимо: {winners_count+1}')
                else:
                    shuffle(participants)
                    winners = participants[:winners_count]
                    for winner in winners:
                        await UsersDrawRepository.set_winner(winner, draw_id)
                    await callback.message.answer('Победители:\n' + '\n'.join([str(user) for user in winners]))
                    await DrawsRepository.end_draw(draw_id)
                    chat_ids = await UsersRepository.get_users_chat_id()
                    for chat_id in chat_ids:
                        await bot.send_message(chat_id, text=f'Розыгрыш {data} завершён. Победители:\n' + '\n'.join([str(user) for user in winners]))


@router.message(Command('start', 'draws'))
async def start(message: Message):
    draws = await DrawsRepository.get_draws()
    markup = main_kb(draws)
    await UsersRepository.add_user(message.from_user.id, message.chat.id)
    if message.text == '/start':
        await message.answer('Добро пожаловать в бот для розыгрышей! Вот список розыгрышей(для участия кликнуть):',
                             reply_markup=markup)
    else:
        await message.answer('Список розыгрышей(для участия кликнуть):', reply_markup=markup)


@router.message(Command('admin_end'))
async def admin_end(message: Message):
    if message.from_user.id == admin:
        draws = await DrawsRepository.get_draws()
        markup = admin_kb(draws)
        await message.answer('Добро пожаловать, администратор! Чтобы завершить розыгрыш нажмите на него',
                             reply_markup=markup)
    else:
        await message.answer('Вы не администратор!')


@router.message(Command('admin_add'))
async def admin_add(message: Message):
    if message.from_user.id == admin:
        try:
            name, winners = message.text.split()[1:]
            winners = int(winners)
            response = await DrawsRepository.add_draw(name, winners)
            if response == 'Error':
                await message.answer('Нельзя добавлять розыгрыши с одинаковым названием!')
            else:
                await message.answer('Розыгрыш успешно добавлен!')
                chat_ids = await UsersRepository.get_users_chat_id()
                for chat_id in chat_ids:
                    sleep(1)
                    await bot.send_message(chat_id, text=f'Новый розыгрыш: {name}!')
        except Exception as e:
            await message.answer('Ошибка ввода данных! Правильный ввод: "/admin_add (название и описание) (кол-во победителей)')
            print(e)
    else:
        await message.answer('Вы не администратор!')