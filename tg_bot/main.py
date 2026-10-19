
Коля Олимов <kolaolimov7@gmail.com>
4:51 PM (0 minutes ago)
to me

import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import aiohttp

# Твой токен бота
TOKEN = "8637573650:AAGRNkfPyBLGiNLKu06KmODmFblVJpsBfTI"

# Настройка логирования
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Состояния для бота (чтобы понимать, когда пользователь ищет что-то конкретное)
class SearchState(StatesGroup):
    waiting_for_query = State()


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Привет! Я твой бот помощник по Minecraft 🎮")


@dp.message(Command("search"))
async def cmd_search(message: types.Message, state: FSMContext):
    await state.set_state(SearchState.waiting_for_query)
    await message.answer(
        "Напиши мне любой вопрос, и я на него отвечу. "
        "Могу даже скинуть фотку, если попросишь! (Например: 'скинь фото котика' или просто задай вопрос)."
    )


@dp.message(SearchState.waiting_for_query, F.text)
async def process_search(message: types.Message, state: FSMContext):
    query = message.text.lower()
    await message.answer("Ищу информацию...")

    # Простая проверка, просит ли пользователь картинку
    if "фото" in query or "картинк" in query or "найди фото" in query:
        # Используем открытое API для картинок (Lorem Picsum или DuckDuckGo/Unsplash)
        # В данном примере для надежности отправляем случайную красивую картинку через фото-апи
        photo_url = f"https://picsum.photos/800/600?random={hash(query) % 1000}"
        await message.answer_photo(
            photo=photo_url,
            caption=f"Вот то, что удалось найти по запросу: {message.text}"
        )
    else:
        # Если это текстовый вопрос, генерируем ответ (или делаем поиск)
        # Здесь можно подключить поиск или ИИ, для примера выдаем базовый ответ
        await message.answer(f"По твоему запросу ('{message.text}'): всё готово! Спрашивай еще или напиши /search для нового поиска.")
    
    # Сбрасываем состояние, чтобы бот вернулся в обычный режим
    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
