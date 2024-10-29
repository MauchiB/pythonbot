import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
import logging
from userprivte.privatechat import router
from db.models import mainsql
from adminbot.admin_user import adminsql
from adminbot.private_admin import admin_router


bot = Bot(token=TOKEN)
db = Dispatcher()

async def main():
    await mainsql()
    await adminsql()
    db.include_routers(router, admin_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await db.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())