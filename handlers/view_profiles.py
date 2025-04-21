import random
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from utils.profile import show_profile
from database import user_data
from keyboards.buttons import reaction_keyboard

router = Router()

# Храним, какую анкету сейчас смотрит пользователь
viewing_index = {}

@router.message(F.text == "👀 Смотреть анкеты")
async def start_viewing(message: Message, state: FSMContext):
    viewer_id = message.from_user.id
    profiles = [uid for uid in user_data if uid != viewer_id]

    if not profiles:
        await message.answer("Нет доступных анкет для просмотра.")
        return

    # Сортируем анкеты сначала по времени создания, затем перемешиваем их случайным образом
    sorted_profiles = sorted(
        [user_data[uid] for uid in profiles],
        key=lambda x: x['created_at'],
        reverse=True
    )
    
    # Перемешиваем анкеты после сортировки
    random.shuffle(sorted_profiles)

    # Обновляем словарь с индексом просмотра для этого пользователя
    viewing_index[viewer_id] = 0
    if sorted_profiles:
        first_profile = sorted_profiles[0]
        await show_profile(message, first_profile)
        await message.answer("Поставьте реакцию:", reply_markup=reaction_keyboard)

@router.callback_query(F.data.in_(["like", "dislike"]))
async def handle_reaction(callback: CallbackQuery):
    viewer_id = callback.from_user.id
    profiles = [uid for uid in user_data if uid != viewer_id]

    index = viewing_index.get(viewer_id, 0)

    # Сортируем анкеты сначала по времени создания, затем перемешиваем их случайным образом
    sorted_profiles = sorted(
        [user_data[uid] for uid in profiles],
        key=lambda x: x['created_at'],
        reverse=True
    )
    
    # Перемешиваем анкеты после сортировки
    random.shuffle(sorted_profiles)

    if index >= len(sorted_profiles):
        await callback.message.edit_text("Вы посмотрели все доступные анкеты.")
        return

    liked_id = sorted_profiles[index]
    viewing_index[viewer_id] = index + 1

    if callback.data == "like":
        liker_profile = user_data[viewer_id]
        await callback.bot.send_photo(
            chat_id=liked_id,
            photo=liker_profile["photo"],
            caption=f"Ваша анкета кому-то понравилась!\n\n"
                    f"{liker_profile['name']}, {liker_profile['age']}, {liker_profile['grade']} класс\n"
                    f"{liker_profile.get('about', '')}\n\n"
                    f"@{callback.from_user.username if callback.from_user.username else 'Ссылка недоступна'}"
        )

    # Показать следующую анкету
    if viewing_index[viewer_id] < len(sorted_profiles):
        next_profile = sorted_profiles[viewing_index[viewer_id]]
        await callback.message.delete()
        await show_profile(callback.message, next_profile)
        await callback.message.answer("Поставьте реакцию:", reply_markup=reaction_keyboard)
    else:
        await callback.message.edit_text("Вы посмотрели все доступные анкеты.")
