from aiogram import executor

from bot import dispatcher
from startup_shutdown import on_startup, on_shutdown

if __name__ == '__main__':
    executor.start_polling(dispatcher=dispatcher,
                           skip_updates=True,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown)
