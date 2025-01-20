from aiogram import types, Dispatcher
from loader import bot
from aiogram.types import ChatType
from datetime import datetime, timedelta
from handlers.encrypt import encrypt_name
from aiogram.dispatcher import FSMContext
from states.my_state import MyState
from aiogram.dispatcher.filters import Text
from keyboards.user_keyboard import get_main_ikb
from aiogram.utils.exceptions import BadRequest
from database.func_with_db.register_user import register
#from Filters.group_filter import IsGroup
import logging

'''-----------------------------------------------------------*FUNC_MUTE_USER*-------------------------------------------------------------------------------------------------------'''


#@dp.message_handler(commands=['mute'])
async def mute_user(message: types.Message) -> None:
    try:
        if message.reply_to_message and message.chat.type != ChatType.PRIVATE and message.reply_to_message.from_user.id != message.from_user.id:
            chat_id = message.chat.id
            user_id = message.reply_to_message.from_user.id
            user_status = (await bot.get_chat_member(chat_id, user_id)).status
            if user_status == 'administrator' or user_status == 'creator':
                await message.answer(message, "Невозможно замутить администратора.")
            else:
                duration = 60 
                args = message.text.split()[1:]
                reason = message.text.split()[2:]
                if args:
                    try:
                        duration = int(args[0])
                        if duration < 1:
                            await bot.send_message(chat_id, "Время должно быть положительным числом.")
                        if duration > 10080:
                            await bot.send_message(chat_id, "Максимальное время - 1 день.")   
                    except ValueError as e:
                        await bot.send_message(chat_id, f"Неправильный формат времени. {str(e)}")
                mute_until = datetime.now() + timedelta(minutes=duration)
                await bot.restrict_chat_member(chat_id, user_id, until_date=mute_until)
                if reason:
                    await bot.send_message(chat_id, 
                                        f"Пользователь {message.reply_to_message.from_user.full_name.title()},\nЗамучен до {mute_until.strftime('%Y-%m-%d %H:%M:%S')}\nПричина: {' '.join(reason)} ")
                else:
                    await bot.send_message(chat_id, 
                                        f"Пользователь {message.reply_to_message.from_user.full_name.title()},\nЗамучен до {mute_until.strftime('%Y-%m-%d %H:%M:%S')}\nПричина: unspecified")
        else:
            await bot.send_message(chat_id, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите замутить.")
    except BadRequest as _ex:
        logging.error(f"Ошибка при выполнении команды 'mute_user': {_ex}")
            
'''-----------------------------------------------------------*FUNC_UNMUTE_USER*-------------------------------------------------------------------------------------------------------'''

#@dp.message_handler(commands=['unmute'])
async def unmute_user(message: types.Message):
    if message.reply_to_message and message.chat.type != ChatType.PRIVATE and message.reply_to_message.from_user.id != message.from_user.id:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = (await bot.get_chat_member(chat_id, user_id)).status
        if user_status in ['administrator', 'creator']:
            await message.answer("Невозможно размутить администратора.")
        else:
            await bot.restrict_chat_member(
                chat_id,
                user_id,
                types.ChatPermissions(True)    
            )
            await message.answer(f"Пользователь {message.reply_to_message.from_user.full_name} размучен.")
    else:
        await message.answer("Эта команда должна быть использована <b>в ответ<b> на сообщение пользователя, которого вы хотите размутить.")
        
'''-----------------------------------------------------------*FUNC_REPORT_USER*-------------------------------------------------------------------------------------------------------'''


#@dp.message_handler(Command(commands='report', prefixes='!'))
async def increase_rep(message: types.Message, state: FSMContext) -> None:
    try:
        if message.reply_to_message:
            
            # берем данные о юзере и шифруем, а затем регистрируем 
            user = message.from_user.id
            user_id = await encrypt_name(user)
            print(user_id)
            await register(user_id)
            
            # загружаем в стейт
            await MyState.id_user_cancel.set()
            async with state.proxy() as data:
                data['initiator_user_id'] = user
                
            await bot.send_message(chat_id=message.chat.id, text='Спасибо за обращение, мы обязательно разберемся!', reply_markup=get_main_ikb())
            data = await state.get_data()
            export_initiator_user_id = data.get('initiator_user_id')
            print(export_initiator_user_id)
        else:
            await bot.send_message(chat_id=message.chat.id, text='Это команда <b>должна быть</b> ответом на сообщение!')
            
    except BadRequest as _ex:
            logging.error(f"Ошибка при выполнении команды 'increase_rep': {_ex}")
        
'''-----------------------------------------------------------*REGISTRATION_ALL_FUNC*-------------------------------------------------------------------------------------------------------'''
         
        
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(mute_user, commands=['mute'])
    dp.register_message_handler(unmute_user, commands=['unmute'])
    dp.register_message_handler(increase_rep, Text(equals="!report"), state='*')
    
     