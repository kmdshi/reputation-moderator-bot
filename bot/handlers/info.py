from aiogram import types, Dispatcher
from loader import bot
from aiogram.dispatcher.filters import Text

#@dp.message_handler(commands=['start'])
async def welcome_user(message: types.Message) -> None:
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_status = (await bot.get_chat_member(chat_id, user_id)).status
    await bot.send_message(chat_id=message.chat.id, text=f'Привет, {user_status}')

#@dp.message_handler(Command(commands='about', prefixes='$'))
async def about_project_info(message: types.Message) -> None:
    await bot.send_message(message.chat.id, text='''my pet-project for СМП''')    
    
    
#@dp.message_handler(Command(commands='help', prefixes='$'))
async def help_info(message: types.Message) -> None:
        await bot.send_message(message.chat.id, text='''Чтобы выбрать пользователя - нужно ответить реплаем на сообщение пользователя или упомянуть его через @ (работает даже если у пользователя нет username).
                            \nОсновные команды:\n/ban - удаляет пользователя из группы с последующим вносом в черный список
                            \n/mute - ограничивает право участвовать в переписке любым образом
                            \n/unmute - убирает ограничение на право участвовать в переписке любым образом
                            \nпо всем вопросам косаемо бота - @helpernow ''')
        
    



def register_handlers_info(dp: Dispatcher):
    dp.register_message_handler(welcome_user, commands=["start"])
    dp.register_message_handler(about_project_info, Text(equals="$about"))
    dp.register_message_handler(help_info, Text(equals="$help"))      