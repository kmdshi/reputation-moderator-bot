from aiogram import types,Dispatcher
from loader import bot, dp, keywords_links  
  

#@dp.message_handler(lambda message: True)
async def filter_messages(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    status =(await bot.get_chat_member(chat_id, user_id)).status
    if status == 'creator' or status == 'administrator':
        pass
    else:
        for word in keywords_links:
            if word in message.text:
                await bot.delete_message(message.chat.id, message.message_id)
                await bot.send_message(message.chat.id, 'такое тут писать запрещено')
                
                
def register_filters_client(dp: Dispatcher):
    dp.register_message_handler(filter_messages, content_types=types.ContentTypes.TEXT)