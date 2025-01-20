'''-----------------------------------------------------------*IMPORTS*-------------------------------------------------------------------------------------------------------'''
import asyncio
import logging
import os

from database.func_with_db.create_tables import create_tables
from aiogram.utils import executor
from loader import dp, bot
from handlers import client, info
from callback import report_process
from Filters import keywords_filter


'''-----------------------------------------------------------*START BOT CONFIG*-------------------------------------------------------------------------------------------------------'''
current_directory = os.path.dirname(os.path.realpath(__file__))
log_path = os.path.join(current_directory, 'utils', 'logs.log')

logging.basicConfig(level=logging.DEBUG, filename=log_path, format='%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]', datefmt='%d/%m/%Y %I:%M:%S',
                    encoding = 'utf-8', filemode='w')

async def on_startup(dp):
    asyncio.create_task(main())
    logging.warning('Бот был запущен')

async def on_shutdown(dp):
    logging.warning('Бот был выключен..')

async def main() -> None:
    try:
        await create_tables()
        client.register_handlers_client(dp)
        info.register_handlers_info(dp)
        report_process.register_callback_client(dp)
        #keywords_filter.register_filters_client(dp)
    except Exception as ex:
        logging.error(ex)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
