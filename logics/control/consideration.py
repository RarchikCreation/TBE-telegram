from aiogram import types, F
from handlers.lead.bot_instance import dp, bot


@dp.callback_query(F.data.startswith("accept_"))
async def accept_application(callback: types.CallbackQuery):
    user_id = int(callback.data.split("_")[1])
    await bot.send_message(user_id, "Отличные новости: ты принят! Поздравляю! Для начала работы ожидай сообщения от нашего представителя и следуй его дальнейшим инструкциям.")
    await callback.message.edit_text(callback.message.text + "\n\n✅ Принято!", reply_markup=None)

@dp.callback_query(F.data.startswith("decline_"))
async def decline_application(callback: types.CallbackQuery):
    user_id = int(callback.data.split("_")[1])
    await bot.send_message(user_id, "Заявка отклонена! \n➖ Пока это немного недостаточно для вступления. Не расстраивайся, попробуй ещё раз через какое-то время.")
    await callback.message.edit_text(callback.message.text + "\n\n❌ Отклонено!", reply_markup=None)