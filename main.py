import asyncio
from handlers.lead.bot_instance import bot, dp
import handlers.database.management
import logics.starting, logics.control.consideration, logics.control.questions

if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot, skip_updates=True))