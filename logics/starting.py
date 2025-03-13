from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from handlers.database.management import has_user_submitted, add_user_to_submitted
from handlers.lead.bot_instance import bot, dp
from logics.file.directories import mentors_info
from settings.config import CHANNEL_ID, GROUP_ID

class Survey(StatesGroup):
    age = State()
    project_source = State()
    work_time = State()
    experience = State()
    mentor_selection = State()
    need_curator = State()


async def check_subscription(user_id):
    member = await bot.get_chat_member(CHANNEL_ID, user_id)
    return member.status in ['member', 'administrator', 'creator']


@dp.message(F.text.lower() == "/start")
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    if has_user_submitted(user_id):
        await message.answer("Вы уже отправили анкету и не можете заполнить её повторно.")
        return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Подписаться", url="https://t.me/tbe_news")],
        [InlineKeyboardButton(text="✅ Я подписался", callback_data="subscribed")]
    ])
    await message.answer("Пожалуйста, подпишитесь на наш канал, чтобы продолжить.", reply_markup=keyboard)

@dp.callback_query(F.data == "subscribed")
async def subscribed_callback(callback: types.CallbackQuery, state: FSMContext):
    if await check_subscription(callback.from_user.id):
        await callback.message.answer("Спасибо за подписку! Теперь ответьте на несколько вопросов.")
        await state.set_state(Survey.age)
        await callback.message.answer("Ваш возраст?")
    else:
        await callback.answer("❌ Вы ещё не подписаны! Подпишитесь и попробуйте снова.", show_alert=True)



def mentor_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="KARTI", callback_data="choose_mentor_karti")],
            [InlineKeyboardButton(text="IMPO$$IBLE", callback_data="choose_mentor_impossible")],
            [InlineKeyboardButton(text="mdma", callback_data="choose_mentor_mdma")],
            [InlineKeyboardButton(text="sedrick", callback_data="choose_mentor_sedrick")]
        ]
    )
    return keyboard


@dp.callback_query(F.data.startswith("info_mentor_"))
async def mentor_info(callback: types.CallbackQuery):
    mentor_key = callback.data.split("_")[-1]
    mentor_text, mentor_photos = mentors_info.get(mentor_key, ("Информация отсутствует", []))

    await callback.message.answer(f"Информация о наставнике {mentor_key}:\n\n{mentor_text}")

    for photo in mentor_photos:
        await bot.send_photo(callback.from_user.id, photo=types.FSInputFile(photo))


@dp.message(Survey.mentor_selection)
async def process_mentor_selection(message: types.Message, state: FSMContext):
    chosen_mentor = message.text.strip().lower()

    if chosen_mentor in ["karti", "impo$$ible", "mdma", "sedrick"]:
        await state.update_data(mentor=chosen_mentor)
        await message.answer(f"Вы выбрали наставника: {chosen_mentor}")

        await send_survey(message.from_user.id, state)
    else:
        await message.answer("Пожалуйста, выберите наставника из списка!")


async def send_survey(user_id: int, state: FSMContext):
    user_data = await state.get_data()

    user = await bot.get_chat(user_id)
    full_name = user.full_name or "не указано"
    username = f"@{user.username}" if user.username else "не указано"

    survey_text = (
        f"Анкета пользователя: {full_name}\n"
        f"ID: {user_id}\n"
        f"Юзернейм: {username}\n"
        f"Возраст: {user_data['age']}\n"
        f"Источник: {user_data['project_source']}\n"
        f"Время на работу: {user_data['work_time']}\n"
        f"Опыт: {user_data['experience']}\n"
        f"Наставник: {user_data.get('mentor', 'не выбран')}"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Принять", callback_data=f"accept_{user_id}"),
                InlineKeyboardButton(text="Отклонить", callback_data=f"decline_{user_id}")
            ]
        ]
    )

    await bot.send_message(GROUP_ID, survey_text, reply_markup=keyboard)
    add_user_to_submitted(user_id)
    await bot.send_message(user_id, "Спасибо! Ваша анкета отправлена на модерацию.", reply_markup=ReplyKeyboardRemove())
    await state.clear()

