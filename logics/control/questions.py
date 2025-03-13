from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from handlers.lead.bot_instance import dp
from logics.starting import Survey, mentor_keyboard, send_survey

@dp.message(Survey.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Survey.project_source)
    await message.answer("Как вы узнали о нашем проекте?")

@dp.message(Survey.project_source)
async def process_project_source(message: types.Message, state: FSMContext):
    await state.update_data(project_source=message.text)
    await state.set_state(Survey.work_time)
    await message.answer("Сколько времени готовы уделять работе?")

@dp.message(Survey.work_time)
async def process_work_time(message: types.Message, state: FSMContext):
    await state.update_data(work_time=message.text)
    await state.set_state(Survey.experience)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
        ],
        resize_keyboard=True
    )

    await message.answer("Есть ли опыт в данной сфере?", reply_markup=keyboard)

@dp.message(Survey.experience)
async def process_experience(message: types.Message, state: FSMContext):
    await state.update_data(experience=message.text)

    await state.set_state(Survey.need_curator)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
        ],
        resize_keyboard=True
    )

    await message.answer("Нужен ли вам куратор?", reply_markup=keyboard)

@dp.message(Survey.need_curator)
async def process_need_curator(message: types.Message, state: FSMContext):
    await state.update_data(need_curator=message.text)

    if message.text.lower() == "да":
        info_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="KARTI", callback_data="info_mentor_karti")],
                [InlineKeyboardButton(text="IMPO$$IBLE", callback_data="info_mentor_impossible")],
                [InlineKeyboardButton(text="mdma", callback_data="info_mentor_mdma")],
                [InlineKeyboardButton(text="sedrick", callback_data="info_mentor_sedrick")]
            ]
        )

        select_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="KARTI")],
                [KeyboardButton(text="IMPO$$IBLE")],
                [KeyboardButton(text="mdma")],
                [KeyboardButton(text="sedrick")]
            ],
            resize_keyboard=True
        )

        await message.answer("Выберите наставника для просмотра информации:", reply_markup=info_keyboard)
        await message.answer("А теперь выберите наставника окончательно:", reply_markup=select_keyboard)
        await state.set_state(Survey.mentor_selection)
    else:
        await message.answer("Анкета отправлена без выбора куратора.")
        await send_survey(message.from_user.id, state)
