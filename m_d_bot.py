import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


# =========================================================
# НАСТРОЙКИ
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Telegram ID менеджера.
# ЗАМЕНИ 123456789 на свой Telegram ID.
ADMIN_ID = 123456789


if not BOT_TOKEN:
    raise ValueError("Не найдена переменная окружения BOT_TOKEN")


# =========================================================
# СОЗДАНИЕ БОТА
# =========================================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# =========================================================
# УСЛУГИ
# =========================================================

SERVICES = {
    "car": {
        "name": "🚗 Дизайн обклейки авто",
        "description": (
            "Разработка дизайна для обклейки автомобиля.\n\n"
            "Подходит для рекламной, брендированной или "
            "декоративной оклейки автомобиля."
        )
    },

    "booklet": {
        "name": "📖 Буклет/Журнал — 1 стр.",
        "description": (
            "Дизайн одной страницы буклета или журнала "
            "с учётом вашего текста, изображений и фирменного стиля."
        )
    },

    "vk": {
        "name": "VK Оформление ВКонтакте",
        "description": (
            "Оформление сообщества ВКонтакте в едином стиле: "
            "визуальная концепция, элементы оформления и графика."
        )
    },

    "consultation": {
        "name": "💬 Консультация — 1 ч 30 мин",
        "description": (
            "Консультация продолжительностью 1 час 30 минут.\n\n"
            "Можно обсудить дизайн, фирменный стиль, упаковку, "
            "брендинг и другие вопросы."
        )
    },

    "package": {
        "name": "📦 Разработка упаковки",
        "description": (
            "Разработка дизайна упаковки с учётом особенностей "
            "продукта, бренда и требований к печати."
        )
    },

    "printing": {
        "name": "🖨️ Разработка полиграфии",
        "description": (
            "Создание дизайна полиграфической продукции: "
            "листовки, рекламные материалы и другие печатные изделия."
        )
    },

    "strategy": {
        "name": "🎯 Бренд-стратегия",
        "description": (
            "Разработка стратегии развития бренда и его визуального "
            "и смыслового позиционирования."
        )
    },

    "naming": {
        "name": "✏️ Нейминг",
        "description": (
            "Разработка названия для компании, продукта, проекта "
            "или нового бренда."
        )
    },

    "branding": {
        "name": "🎨 Разработка фирменного стиля и брендбука",
        "description": (
            "Создание полноценного фирменного стиля и брендбука "
            "с правилами использования элементов бренда."
        )
    },

    "eurobooklet": {
        "name": "📄 Евробуклет — 1/2/3 фальца (сгиба)",
        "description": (
            "Разработка дизайна евробуклета с 1, 2 или 3 фальцами "
            "(сгибами)."
        )
    },

    "business_card": {
        "name": "💳 Визитка",
        "description": (
            "Разработка дизайна визитной карточки "
            "в соответствии с вашим стилем и задачами."
        )
    },

    "cup": {
        "name": "🥤 Дизайн стакана",
        "description": (
            "Создание дизайна стакана для бренда, кафе, ресторана "
            "или другого проекта."
        )
    },

    "presentation": {
        "name": "📊 Презентация — 1 слайд",
        "description": (
            "Дизайн одного слайда презентации "
            "с аккуратной компоновкой текста, графики и изображений."
        )
    },

    "menu": {
        "name": "🍽️ Дизайн меню",
        "description": (
            "Разработка дизайна меню для кафе, ресторана, бара "
            "или другого заведения."
        )
    },

    "certificate": {
        "name": "🎁 Подарочный сертификат",
        "description": (
            "Разработка дизайна подарочного сертификата "
            "в фирменном стиле."
        )
    }
}


# =========================================================
# КЛАВИАТУРА С УСЛУГАМИ
# =========================================================

def services_keyboard():
    buttons = []

    for service_id, service in SERVICES.items():
        buttons.append([
            InlineKeyboardButton(
                text=service["name"],
                callback_data=f"service:{service_id}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


# =========================================================
# КЛАВИАТУРА УСЛУГИ
# =========================================================

def service_keyboard(service_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📝 Заказать услугу",
                    callback_data=f"order:{service_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад к услугам",
                    callback_data="back_services"
                )
            ]
        ]
    )


# =========================================================
# START
# =========================================================

@dp.message(CommandStart())
async def start_command(message: Message):

    text = (
        "Здравствуйте! 👋\n\n"
        "Мы — команда дизайнеров.\n"
        "Поможем создать дизайн под ваши задачи: "
        "от визитки до полноценного фирменного стиля.\n\n"
        "Выберите интересующую вас услугу ниже 👇"
    )

    await message.answer(
        text,
        reply_markup=services_keyboard()
    )


# =========================================================
# НАЖАТИЕ НА УСЛУГУ
# =========================================================

@dp.callback_query(F.data.startswith("service:"))
async def service_selected(callback: CallbackQuery):

    service_id = callback.data.split(":", 1)[1]

    if service_id not in SERVICES:
        await callback.answer(
            "Услуга не найдена",
            show_alert=True
        )
        return

    service = SERVICES[service_id]

    text = (
        f"<b>{service['name']}</b>\n\n"
        f"{service['description']}\n\n"
        "Если хотите заказать эту услугу, нажмите кнопку ниже 👇"
    )

    await callback.message.edit_text(
        text,
        reply_markup=service_keyboard(service_id),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================================
# НАЗАД К СПИСКУ УСЛУГ
# =========================================================

@dp.callback_query(F.data == "back_services")
async def back_services(callback: CallbackQuery):

    text = (
        "Выберите интересующую вас услугу 👇"
    )

    await callback.message.edit_text(
        text,
        reply_markup=services_keyboard()
    )

    await callback.answer()


# =========================================================
# ЗАКАЗ УСЛУГИ
# =========================================================

@dp.callback_query(F.data.startswith("order:"))
async def order_service(callback: CallbackQuery):

    service_id = callback.data.split(":", 1)[1]

    if service_id not in SERVICES:
        await callback.answer(
            "Услуга не найдена",
            show_alert=True
        )
        return

    service = SERVICES[service_id]

    # Сохраняем выбранную услугу для конкретного пользователя
    user_orders[callback.from_user.id] = service_id

    await callback.message.answer(
        f"Вы выбрали:\n\n"
        f"<b>{service['name']}</b>\n\n"
        "Теперь напишите одним сообщением, что именно вам нужно "
        "и, если есть, укажите дополнительные пожелания.\n\n"
        "Например:\n"
        "«Нужно сделать дизайн визитки для строительной компании. "
        "Есть логотип и фирменные цвета.»",
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================================
# ХРАНЕНИЕ СОСТОЯНИЯ ЗАКАЗОВ
# =========================================================

user_orders = {}


# =========================================================
# ПОЛУЧЕНИЕ СООБЩЕНИЯ ОТ КЛИЕНТА
# =========================================================

@dp.message()
async def receive_order(message: Message):

    user_id = message.from_user.id

    # Если пользователь не выбирал услугу
    if user_id not in user_orders:

        await message.answer(
            "Сначала выберите интересующую вас услугу 👇",
            reply_markup=services_keyboard()
        )

        return

    service_id = user_orders[user_id]
    service = SERVICES[service_id]

    username = (
        f"@{message.from_user.username}"
        if message.from_user.username
        else "нет username"
    )

    full_name = message.from_user.full_name

    # =====================================================
    # ЗАЯВКА МЕНЕДЖЕРУ
    # =====================================================

    admin_text = (
        "🔔 <b>НОВАЯ ЗАЯВКА</b>\n\n"
        f"👤 Клиент: {full_name}\n"
        f"🔗 Username: {username}\n"
        f"🆔 Telegram ID: <code>{user_id}</code>\n\n"
        f"📌 <b>Услуга:</b>\n"
        f"{service['name']}\n\n"
        f"💬 <b>Сообщение клиента:</b>\n"
        f"{message.text}"
    )

    try:

        await bot.send_message(
            ADMIN_ID,
            admin_text,
            parse_mode="HTML"
        )

        # =================================================
        # ОТВЕТ КЛИЕНТУ
        # =================================================

        await message.answer(
            "✅ Спасибо! Ваша заявка отправлена менеджеру.\n\n"
            "Менеджер ознакомится с сообщением и свяжется "
            "с вами для уточнения деталей."
        )

        # Удаляем выбранную услугу после отправки заявки
        del user_orders[user_id]

    except Exception as error:

        print("Ошибка отправки заявки:", error)

        await message.answer(
            "❌ Не удалось отправить заявку менеджеру.\n\n"
            "Попробуйте ещё раз немного позже."
        )


# =========================================================
# ЗАПУСК
# =========================================================

async def main():

    print("===================================")
    print("      БОТ УСПЕШНО ЗАПУЩЕН")
    print("===================================")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())