from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# Кнопка "Заполнить анкету"
fill_form_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Заполнить анкету")]
    ],
    resize_keyboard=True
)

# Кнопки после заполнения анкеты
after_fill_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👀 Смотреть анкеты")],
        [KeyboardButton(text="✏️ Изменить анкету")],
        [KeyboardButton(text="⛔️ Остановить анкету")]
    ],
    resize_keyboard=True
)

# Кнопка "Пропустить"
skip_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Пропустить")]
    ],
    resize_keyboard=True
)

# Кнопки изменения анкеты
edit_options_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Изменить имя")],
        [KeyboardButton(text="Изменить возраст")],
        [KeyboardButton(text="Изменить класс")],
        [KeyboardButton(text="Изменить фото")],
        [KeyboardButton(text="Изменить описание")]
    ],
    resize_keyboard=True
)

# Кнопка для просмотра анкет
view_profiles_button = KeyboardButton(text="👀 Смотреть анкеты")

# Кнопки лайк и дизлайк для реакции на анкеты
reaction_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="❤️", callback_data="like"),
        InlineKeyboardButton(text="❌", callback_data="dislike")
    ]
])
# Кнопки лайк и дизлайк для реакции на анкеты
reaction_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="❤️", callback_data="like"),
        InlineKeyboardButton(text="❌", callback_data="dislike")
    ]
])
