from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from core.utils.statesform import StepsForm


async def get_form(message: Message, state: FSMContext):
    await message.answer(
        f"{message.from_user.first_name}, начнем заполнять анкету. Введите ваше имя: "
    )
    await state.set_state(StepsForm.GET_NAME)


async def get_name(message: Message, state: FSMContext):
    await message.answer(f"Твое имя: \r\n{message.text}\r\nТеперь введи фамилию:")
    await state.update_data(name=message.text)
    await state.set_state(StepsForm.GET_LAST_NAME)


async def get_last_name(message: Message, state: FSMContext):
    await message.answer(f"Ваша Фамилия: \r\n{message.text}\r\nТеперь введите возраст:")
    await state.update_data(last_name=message.text)
    await state.set_state(StepsForm.GET_AGE)


async def get_age(message: Message, state: FSMContext):
    if message.text.isdigit():
        await message.answer(f"Ваш возраст \r\n{message.text}\r\t")
        context_data = await state.get_data()
        await message.answer(
            f"Сохраненные данные в машине состояний: {str(context_data)}"
        )
        name = context_data.get("name")
        last_name = context_data.get("last_name")
        data_user = (
            f"Вот твои данные\r\n"
            f"Ваше имя: {name}\r\n"
            f"Ваша фамилия: {last_name}\r\n"
            f"Ваш возраст: {message.text}\r\n"
        )
        await message.answer(data_user)
        await state.clear()
    else:
        await message.answer(f"Возраст должен быть указан цифрами! Повторите ввод.")
