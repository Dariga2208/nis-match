from datetime import datetime

# Словарь для хранения данных пользователей
user_data = {}

# Функция для добавления анкеты пользователя
def add_profile(user_id, name, age, grade, about):
    profile = {
        "name": name,
        "age": age,
        "grade": grade,
        "about": about,
        "created_at": datetime.now()  # Добавляем временную метку для сортировки
    }
    user_data[user_id] = profile

# Функция для получения всех анкет
def get_profiles():
    return user_data

# Пример добавления анкет
add_profile(123, "Дарига", 18, "12 класс", "Люблю путешествовать")
add_profile(456, "Айжан", 17, "11 класс", "Интересуюсь программированием")
