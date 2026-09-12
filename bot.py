import os

from aiogram import Bot, Dispatcher, executor, types


BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "Здравствуйте! 👋\n\n"
        "Бот успешно работает!"
    )


if __name__ == "__main__":
    print("Бот запускается...")
    executor.start_polling(dp, skip_updates=True)
