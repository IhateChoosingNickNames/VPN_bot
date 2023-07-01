from aiogram import Bot, Dispatcher, executor, types

import settings
from db.queries import get_info

admin_bot = Bot(token=settings.ADMIN_BOT_TOKEN)
dp = Dispatcher(admin_bot)


def start_admin_bot():
    """Инициализация админского бота."""
    executor.start_polling(dp, skip_updates=False)


@dp.message_handler(regexp="/start")
async def bot_start(message: types.Message):
    """Начало работы."""
    if str(message["from"]["id"]) not in settings.ADMIN_IDs:
        await message.answer("У вас недостаточно прав")
    else:
        for elem in get_info():
            await message.answer(elem)
