from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ChatMemberAdministrator
from database.func_with_db.increase_rep import reverse_add_reputation
from database.func_with_db.add_rep import add_reputation
from database.func_with_db.check_rep import check_reputation
import logging

from handlers.encrypt import encrypt_name
from loader import dp, bot
from random import randint  
#from Filters.group_filter import IsGroup

'''-----------------------------------------------------------*CANCEL_REPORT_ADMIN*-------------------------------------------------------------------------------------------------------'''

async def cancel_report_admin(call: types.CallbackQuery, state: FSMContext):
    try:    
        
        # данные о юзере который нажал на кнопку
        chat_id = call.message.chat.id
        user = call.from_user.id
        message_id = call.message.message_id
        call_user_status = (await bot.get_chat_member(chat_id, user)).status
        
        # выгружаем данные из стейта
        data = await state.get_data()
        export_initiator_user_id = data.get('initiator_user_id')
        print(export_initiator_user_id)
        chat_member = await bot.get_chat_member(chat_id, export_initiator_user_id)
        user_name = chat_member.user.full_name  

        
        # шифруем
        initiator_user_id = await encrypt_name(export_initiator_user_id)

        if call_user_status in ['administrator', 'creator', 'owner']:
            
            # удаляем сообщение с выбором кнопок
            await bot.delete_message(chat_id, call.message.message_id)
            
            # выбираем значение для репутации
            num = randint(0, 15)
            
            # меняем репутацию, а затем берем её из дб
            await reverse_add_reputation(initiator_user_id, num)
            reputation = await check_reputation(initiator_user_id)
            
            # оповещаем
            await bot.send_message(chat_id, f'Пользователю {user_name} уменьшили репутацию, текущее количество репутации - {reputation} (-{num})')
            await call.answer('Репорт успешно удален.', show_alert=True)
        else:
            await call.answer('У вас недостаточно прав на это действие.', show_alert=True)    
            
    except Exception as ex:
        logging.error(f"Ошибка при выполнении кал-бек команды 'cancel_report_admin': {ex}")

'''-----------------------------------------------------------*ACCEPT_REPORT_ADMIN*-------------------------------------------------------------------------------------------------------'''
    
async def accept_report_admin(call: types.CallbackQuery, state: FSMContext):
    try:
        
        # данные о юзере который нажал на кнопку
        chat_id = call.message.chat.id
        user = call.from_user.id
        message_id = call.message.message_id
        call_user_status = (await bot.get_chat_member(chat_id, user)).status
        
        # выгружаем данные из стейта
        data = await state.get_data()
        export_initiator_user_id = data.get('initiator_user_id')
        print(export_initiator_user_id)
        chat_member = await bot.get_chat_member(chat_id, export_initiator_user_id)
        user_name = chat_member.user.full_name  

        # шифруем
        initiator_user_id = await encrypt_name(export_initiator_user_id)
        print(initiator_user_id)
        if call_user_status in ['administrator', 'creator', 'owner']:
            # удаляем сообщение с выбором кнопок
            await bot.delete_message(chat_id, message_id)
            
            # выбираем значение для репутации
            num = randint(0, 15)
            
            #меняем репутацию, а затем берем её из дб
            await add_reputation(initiator_user_id, num)
            reputation = await check_reputation(initiator_user_id)
            
            # оповещаем
            await bot.send_message(chat_id, f'Пользователю {user_name} увеличили репутацию, текущее количество репутации - {reputation} (+{num})')
            await call.answer('Репорт успешно удален.', show_alert=True)
        else:
            await call.answer('У вас недостаточно прав на это действие.', show_alert=True)   
    except Exception as ex:
        logging.error(f"Ошибка при выполнении кал-бек команды 'accept_report_admin': {ex}")

  
'''-----------------------------------------------------------*CANCEL_REPORT_USER*-------------------------------------------------------------------------------------------------------'''

#@dp.callback_query_handler(lambda call: call.data == 'cancel_action', state='*')
async def cancel_report_user(call: types.CallbackQuery, state: FSMContext) -> None:
    try:
        chat_id = call.message.chat.id
        user = call.from_user.id 
        data = await state.get_data()
        initiator_user_id = data.get('initiator_user_id')
        print(initiator_user_id)
        message_id = call.message.message_id
        if initiator_user_id is not None and initiator_user_id == user:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
            await bot.delete_message(chat_id, message_id)
            await call.answer('Репорт успешно отозван.', show_alert=True)
        else:
            await call.answer('Вы не можете отменить этот репорт.', show_alert=True)
        
        await state.finish()
    except Exception as ex:
        logging.error(f"Ошибка при выполнении кал-бек команды 'cancel_report_user': {ex}")
        
'''-----------------------------------------------------------*REGISTRATION_ALL_CALLBACKS*-------------------------------------------------------------------------------------------------------'''
            
def register_callback_client(dp: Dispatcher):
    dp.register_callback_query_handler(cancel_report_user,lambda call: call.data == 'cancel_action', state='*')
    dp.register_callback_query_handler(cancel_report_admin,lambda call: call.data == 'cancel_action_admin', state='*')
    dp.register_callback_query_handler(accept_report_admin,lambda call: call.data == 'accept_action_admin', state='*')