from aiogram import Router, F
from aiogram.types import Message, ContentType, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.buttons import (
    fill_form_button, after_fill_keyboard,
    skip_button, edit_options_keyboard, reaction_keyboard, view_profiles_button
)
from utils.profile import show_profile
from database import user_data
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hlink

router = Router()

# Этапы анкеты
class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()
    photo = State()
    about = State()

class EditForm(StatesGroup):
    name = State()
    age = State()
    grade = State()
    photo = State()
    about = State()

# Отслеживаем текущую позицию пользователя при просмотре анкет
viewing_progress = {}

@router.message(F.text == "/start")
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    profile = user_data.get(user_id)

    if profile:
        await show_profile(message, profile)
        await message.answer("Вы можете изменить или остановить анкету:", reply_markup=after_fill_keyboard)
    else:
        await message.answer("Привет! Нажми кнопку ниже, чтобы заполнить анкету:", reply_markup=fill_form_button)

@router.message(F.text == "📋 Заполнить анкету")
async def ask_name(message: Message, state: FSMContext):
    await message.answer("Как вас называть?", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.name)

@router.message(Form.name)
async def ask_age(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько вам лет?")
    await state.set_state(Form.age)

@router.message(Form.age)
async def ask_grade(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("В каком ты классе?")
    await state.set_state(Form.grade)

@router.message(Form.grade)
async def ask_photo(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    await message.answer("Отправьте свою фотографию.")
    await state.set_state(Form.photo)

@router.message(Form.photo, F.photo)
async def ask_about(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    await message.answer("Теперь напишите немного о себе. Можешь нажать 'Пропустить', если не хочешь писать.", reply_markup=skip_button)
    await state.set_state(Form.about)

@router.message(Form.about, F.text.lower() == "пропустить")
async def skip_about(message: Message, state: FSMContext):
    await state.update_data(about="")
    await finish_form(message, state)

@router.message(Form.about)
async def finish(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await finish_form(message, state)

async def finish_form(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    user_data[user_id] = {
        "user_id": user_id,  # 👈 обязательно добавляем!
        "name": data["name"],
        "age": data["age"],
        "grade": data["grade"],
        "photo": data["photo"] if data.get("photo") else None,  # Обрабатываем отсутствие фото
        "about": data.get("about", ""),
    }
    await show_profile(message, data)
    await message.answer("Анкета сохранена!", reply_markup=after_fill_keyboard)
    await state.clear()

# Остановить анкету
@router.message(F.text == "⛔️ Остановить анкету")
async def stop_profile(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in user_data:
        del user_data[user_id]
    await state.clear()
    await message.answer("Анкета удалена. Нажми кнопку ниже, чтобы начать заново.", reply_markup=fill_form_button)

# Кнопка Изменить анкету
@router.message(F.text == "✏️ Изменить анкету")
async def edit_profile_menu(message: Message):
    await message.answer("Что вы хотите изменить?", reply_markup=edit_options_keyboard)

@router.message(F.text == "Изменить имя")
async def edit_name(message: Message, state: FSMContext):
    await message.answer("Введите новое имя:")
    await state.set_state(EditForm.name)

@router.message(EditForm.name)
async def save_new_name(message: Message, state: FSMContext):
    user_data[message.from_user.id]["name"] = message.text
    await show_profile(message, user_data[message.from_user.id])
    await message.answer("Имя обновлено!", reply_markup=after_fill_keyboard)
    await state.clear()

@router.message(F.text == "Изменить возраст")
async def edit_age(message: Message, state: FSMContext):
    await message.answer("Введите новый возраст:")
    await state.set_state(EditForm.age)

@router.message(EditForm.age)
async def save_new_age(message: Message, state: FSMContext):
    user_data[message.from_user.id]["age"] = message.text
    await show_profile(message, user_data[message.from_user.id])
    await message.answer("Возраст обновлён!", reply_markup=after_fill_keyboard)
    await state.clear()

@router.message(F.text == "Изменить класс")
async def edit_grade(message: Message, state: FSMContext):
    await message.answer("Введите новый класс:")
    await state.set_state(EditForm.grade)

@router.message(EditForm.grade)
async def save_new_grade(message: Message, state: FSMContext):
    user_data[message.from_user.id]["grade"] = message.text
    await show_profile(message, user_data[message.from_user.id])
    await message.answer("Класс обновлён!", reply_markup=after_fill_keyboard)
    await state.clear()

@router.message(F.text == "Изменить фото")
async def edit_photo(message: Message, state: FSMContext):
    await message.answer("Отправьте новое фото:")
    await state.set_state(EditForm.photo)

@router.message(EditForm.photo, F.photo)
async def save_new_photo(message: Message, state: FSMContext):
    user_data[message.from_user.id]["photo"] = message.photo[-1].file_id
    await show_profile(message, user_data[message.from_user.id])
    await message.answer("Фото обновлено!", reply_markup=after_fill_keyboard)
    await state.clear()

@router.message(F.text == "Изменить описание")
async def edit_about(message: Message, state: FSMContext):
    await message.answer("Напишите новый текст о себе:")
    await state.set_state(EditForm.about)

@router.message(EditForm.about)
async def save_new_about(message: Message, state: FSMContext):
    user_data[message.from_user.id]["about"] = message.text
    await show_profile(message, user_data[message.from_user.id])
    await message.answer("Описание обновлено!", reply_markup=after_fill_keyboard)
    await state.clear()

# Отслеживаем просмотр анкет
@router.message(F.text == "👀 Смотреть анкеты")
async def view_profiles(message: Message):
    user_id = message.from_user.id
    candidates = [uid for uid in user_data if uid != user_id]

    if not candidates:
        await message.answer("Пока нет других анкет для просмотра.")
        return

    viewing_progress[user_id] = {"candidates": candidates, "index": 0}
    await show_next_candidate(message, user_id)

async def show_next_candidate(message: Message, viewer_id: int):
    progress = viewing_progress.get(viewer_id)
    if not progress or progress["index"] >= len(progress["candidates"]):
        await message.answer("Анкеты закончились!")
        viewing_progress.pop(viewer_id, None)
        return

    candidate_id = progress["candidates"][progress["index"]]
    profile = user_data.get(candidate_id)

    if not profile or not profile.get('photo'):
        await message.answer("У этого пользователя нет фото.")
        return

    caption = f"{profile['name']}, {profile['age']}, {profile['grade']} класс\n\n{profile['about']}"
    await message.answer_photo(photo=profile['photo'], caption=caption, reply_markup=reaction_keyboard)

    # сохраняем текущую анкету
    progress["current"] = candidate_id

@router.callback_query(F.data == "like")
async def handle_like(callback: CallbackQuery):
    liker_id = callback.from_user.id
    progress = viewing_progress.get(liker_id)

    if not progress:
        await callback.answer("Нет анкеты для лайка.")
        return

    liked_id = progress["current"]
    if liked_id in user_data:
        liker_profile = user_data[liker_id]
        caption = f"{liker_profile['name']}, {liker_profile['age']}, {liker_profile['grade']} класс\n\n{liker_profile['about']}"
        link = hlink("Открыть профиль", f"tg://user?id={liker_id}")

        await callback.bot.send_photo(
            chat_id=liked_id,
            photo=liker_profile['photo'],
            caption=f"❤️ Твоя анкета кому-то понравилась!\n\n{caption}\n\n{link}"
        )

    progress["index"] += 1
    await show_next_candidate(callback.message, liker_id)

@router.callback_query(F.data == "dislike")
async def handle_dislike(callback: CallbackQuery):
    user_id = callback.from_user.id
    progress = viewing_progress.get(user_id)
    if progress:
        progress["index"] += 1
        await show_next_candidate(callback.message, user_id)
