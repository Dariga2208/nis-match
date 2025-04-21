from aiogram.types import Message, InputMediaPhoto

async def show_profile(message: Message, data: dict):
    text = f"{data.get('name', '—')}, {data.get('age', '—')} лет, {data.get('grade', '—')} класс\n\n"
    about = data.get("about", "").strip()
    if about:
        text += about

    await message.answer_photo(photo=data["photo"], caption=text)
