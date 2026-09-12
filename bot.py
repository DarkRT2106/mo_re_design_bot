import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# =========================================================
# НАСТРОЙКИ
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ЗАМЕНИ НА TELEGRAM ID АДМИНИСТРАТОРА
ADMIN_ID = 1218273433


if not BOT_TOKEN:
    raise ValueError("Не найдена переменная окружения BOT_TOKEN")


# =========================================================
# СОЗДАНИЕ БОТА
# =========================================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


# =========================================================
# ОСНОВНЫЕ УСЛУГИ
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

    "vk": {
        "name": "VK Оформление ВКонтакте",
        "description": (
            "Оформление сообщества ВКонтакте в едином стиле.\n\n"
            "Разработка визуальной концепции, графики и "
            "необходимых элементов оформления."
        )
    },

    "consultation": {
        "name": "💬 Консультация — 1 ч 30 мин",
        "description": (
            "Консультация продолжительностью 1 час 30 минут.\n\n"
            "Можно обсудить дизайн, фирменный стиль, брендинг, "
            "упаковку, полиграфию и другие вопросы."
        )
    },

    "package": {
        "name": "📦 Разработка упаковки",
        "description": (
            "Разработка дизайна упаковки с учётом особенностей "
            "продукта, бренда и требований к печати."
        )
    },

    "strategy": {
        "name": "🎯 Бренд-стратегия",
        "description": (
            "Разработка стратегии развития бренда, "
            "его позиционирования и визуального направления."
        )
    },

    "naming": {
        "name": "✏️ Нейминг",
        "description": (
            "Разработка названия для компании, продукта, "
            "проекта или нового бренда."
        )
    },

    "branding": {
        "name": "🎨 Разработка фирменного стиля и брендбука",
        "description": (
            "Создание полноценного фирменного стиля и брендбука "
            "с правилами использования элементов бренда."
        )
    }
}


# =========================================================
# ПОЛИГРАФИЯ
# =========================================================

PRINTING_SERVICES = {

    "business_card": {
        "name": "📇 Визитка",
        "description": (
            "Разработка дизайна визитной карточки "
            "в соответствии с вашим стилем и задачами."
        )
    },

    "flyer": {
        "name": "📄 Листовка",
        "description": (
            "Дизайн рекламной или информационной листовки "
            "для печати."
        )
    },

    "flyer_small": {
        "name": "📋 Флаер",
        "description": (
            "Разработка дизайна флаера для рекламы, "
            "мероприятий, акций или специальных предложений."
        )
    },

    "booklet": {
        "name": "📖 Буклет",
        "description": (
            "Разработка дизайна буклета с учётом текста, "
            "изображений и фирменного стиля."
        )
    },

    "magazine": {
        "name": "📰 Журнал",
        "description": (
            "Разработка дизайна страниц журнала "
            "и их визуального оформления."
        )
    },

    "eurobooklet": {
        "name": "📑 Евробуклет — 1/2/3 фальца",
        "description": (
            "Разработка дизайна евробуклета "
            "с 1, 2 или 3 фальцами (сгибами)."
        )
    },

    "poster": {
        "name": "🖼️ Плакат",
        "description": (
            "Разработка дизайна плаката для рекламы, "
            "мероприятия или информационной кампании."
        )
    },

    "certificate": {
        "name": "🎁 Подарочный сертификат",
        "description": (
            "Разработка дизайна подарочного сертификата "
            "в фирменном стиле."
        )
    },

    "menu": {
        "name": "🍽️ Меню",
        "description": (
            "Разработка дизайна меню для кафе, ресторана, "
            "бара или другого заведения."
        )
    },

    "label": {
        "name": "🏷️ Этикетка",
        "description": (
            "Разработка дизайна этикетки для продукции "
            "с учётом требований к печати."
        )
    },

    "sticker": {
        "name": "🔖 Наклейка",
        "description": (
            "Разработка дизайна наклейки для бренда, "
            "товара, упаковки или рекламных целей."
        )
    },

    "catalog": {
        "name": "🗂️ Каталог",
        "description": (
            "Разработка дизайна каталога продукции, "
            "товаров или услуг."
        )
    },

    "brochure": {
        "name": "📚 Брошюра",
        "description": (
            "Разработка дизайна брошюры "
            "с оформлением текста и графики."
        )
    },

    "envelope": {
        "name": "✉️ Конверт",
        "description": (
            "Разработка дизайна фирменного или "
            "рекламного конверта."
        )
    },

    "cup": {
        "name": "🥤 Дизайн стакана",
        "description": (
            "Разработка дизайна стакана для кафе, "
            "ресторана, бренда или мероприятия."
        )
    },

    "other": {
        "name": "➕ Другое",
        "description": (
            "Если вам нужно что-то, чего нет в списке, "
            "выберите этот вариант и опишите задачу."
        )
    }
}


# =========================================================
# ХРАНЕНИЕ СОСТОЯНИЯ ПОЛЬЗОВАТЕЛЕЙ
# =========================================================

user_orders = {}


# =========================================================
# ГЛАВНОЕ МЕНЮ
# =========================================================

def main_menu_keyboard():

    buttons = []

    for service_id, service in SERVICES.items():

        buttons.append([
            InlineKeyboardButton(
                text=service["name"],
                callback_data=f"service:{service_id}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="🖨️ Разработка полиграфии",
            callback_data="printing_menu"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


# =========================================================
# МЕНЮ ПОЛИГРАФИИ
# =========================================================

def printing_menu_keyboard():

    buttons = []

    for service_id, service in PRINTING_SERVICES.items():

        buttons.append([
            InlineKeyboardButton(
                text=service["name"],
                callback_data=f"printing:{service_id}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="⬅️ Назад к услугам",
            callback_data="back_main"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


# =========================================================
# КНОПКИ КОНКРЕТНОЙ УСЛУГИ
# =========================================================

def service_keyboard(service_id, printing=False):

    prefix = "printing" if printing else "service"

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="📝 Заказать услугу",
                    callback_data=f"order:{prefix}:{service_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=(
                        "back_printing"
                        if printing
                        else "back_main"
                    )
                )
            ]

        ]
    )


# =========================================================
# /START
# =========================================================

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):

    text = (
        "Здравствуйте! 👋\n\n"
        "Мы — команда дизайнеров.\n"
        "Поможем создать дизайн под ваши задачи: "
        "от полиграфии до полноценного фирменного стиля.\n\n"
        "Выберите интересующую вас услугу ниже 👇"
    )

    await message.answer(
        text,
        reply_markup=main_menu_keyboard()
    )


# =========================================================
# ОТКРЫТИЕ ПОЛИГРАФИИ
# =========================================================

@dp.callback_query_handler(lambda callback: callback.data == "printing_menu")
async def open_printing_menu(callback: types.CallbackQuery):

    text = (
        "🖨️ <b>Разработка полиграфии</b>\n\n"
        "Что именно вам нужно разработать?\n\n"
        "Выберите подходящий вариант ниже 👇"
    )

    await callback.message.edit_text(
        text,
        reply_markup=printing_menu_keyboard(),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================================
# ВЫБОР ОСНОВНОЙ УСЛУГИ
# =========================================================

@dp.callback_query_handler(
    lambda callback: callback.data.startswith("service:")
)
async def service_selected(callback: types.CallbackQuery):

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
        "Если хотите заказать эту услугу, "
        "нажмите кнопку ниже 👇"
    )

    await callback.message.edit_text(
        text,
        reply_markup=service_keyboard(service_id),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================================
# ВЫБОР УСЛУГИ ПОЛИГРАФИИ
# =========================================================

@dp.callback_query_handler(
    lambda callback: callback.data.startswith("printing:")
)
async def printing_selected(callback: types.CallbackQuery):

    service_id = callback.data.split(":", 1)[1]

    if service_id not in PRINTING_SERVICES:

        await callback.answer(
            "Услуга не найдена",
            show_alert=True
        )

        return

    service = PRINTING_SERVICES[service_id]

    text = (
        f"<b>{service['name']}</b>\n\n"
        f"{service['description']}\n\n"
        "Если хотите заказать эту услугу, "
        "нажмите кнопку ниже 👇"
    )

    await callback.message.edit_text(
        text,
        reply_markup=service_keyboard(
            service_id,
            printing=True
        ),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================================
# НАЗАД В ГЛАВНОЕ МЕНЮ
# =========================================================

@dp.callback_query_handler(
    lambda callback: callback.data == "back_main"
)
async def back_main(callback: types.CallbackQuery):

    text = "Выберите интересующую вас услугу 👇"

    await callback.message.edit_text(
        text,
        reply_markup=main_menu_keyboard()
    )

    await callback.answer()


# =========================================================
# НАЗАД В ПОЛИГРАФИЮ
# =========================================================

@dp.callback_query_handler(
    lambda callback: callback.data == "back_printing"
)
async def back_printing(callback: types.CallbackQuery):

    text = (
        "🖨️ <b>Разработка полиграфии</b>\n\n"
        "Что именно вам нужно разработать?\n\n"
        "Выберите подходящий вариант ниже 👇"
    )

    await callback.message.edit_text(
        text,
        reply_markup=printing_menu_keyboard(),
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================================
# ЗАКАЗ ОСНОВНОЙ УСЛУГИ
# =========================================================

@dp.callback_query_handler(
    lambda callback: callback.data.startswith("order:service:")
)
async def order_main_service(callback: types.CallbackQuery):

    service_id = callback.data.split(":", 2)[2]

    if service_id not in SERVICES:

        await callback.answer(
            "Услуга не найдена",
            show_alert=True
        )

        return

    service = SERVICES[service_id]

    user_orders[callback.from_user.id] = {
        "name": service["name"],
        "category": "Основная услуга"
    }

    await callback.message.answer(
        f"Вы выбрали:\n\n"
        f"<b>{service['name']}</b>\n\n"
        "Теперь напишите одним сообщением, "
        "что именно вам нужно и какие есть пожелания.\n\n"
        "Например:\n"
        "«Нужно разработать фирменный стиль "
        "для новой компании. Есть логотип и "
        "фирменные цвета.»",
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================================
# ЗАКАЗ ПОЛИГРАФИИ
# =========================================================

@dp.callback_query_handler(
    lambda callback: callback.data.startswith("order:printing:")
)
async def order_printing_service(callback: types.CallbackQuery):

    service_id = callback.data.split(":", 2)[2]

    if service_id not in PRINTING_SERVICES:

        await callback.answer(
            "Услуга не найдена",
            show_alert=True
        )

        return

    service = PRINTING_SERVICES[service_id]

    user_orders[callback.from_user.id] = {
        "name": service["name"],
        "category": "Полиграфия"
    }

    await callback.message.answer(
        f"Вы выбрали:\n\n"
        f"<b>{service['name']}</b>\n\n"
        "Теперь напишите одним сообщением, "
        "что именно вам нужно и какие есть пожелания.\n\n"
        "Например:\n"
        "«Нужна визитка для компании. "
        "Есть логотип, контакты и фирменные цвета.»",
        parse_mode="HTML"
    )

    await callback.answer()


# =========================================================
# ПОЛУЧЕНИЕ ЗАЯВКИ
# =========================================================

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def receive_order(message: types.Message):

    user_id = message.from_user.id

    # -----------------------------------------------------
    # Если пользователь ничего не выбирал
    # -----------------------------------------------------

    if user_id not in user_orders:

        await message.answer(
            "Сначала выберите интересующую вас услугу 👇",
            reply_markup=main_menu_keyboard()
        )

        return

    order = user_orders[user_id]

    service_name = order["name"]
    category = order["category"]

    username = (
        f"@{message.from_user.username}"
        if message.from_user.username
        else "нет username"
    )

    full_name = message.from_user.full_name

    # -----------------------------------------------------
    # Сообщение менеджеру
    # -----------------------------------------------------

    admin_text = (
        "🔔 <b>НОВАЯ ЗАЯВКА</b>\n\n"

        f"👤 <b>Клиент:</b> {full_name}\n"
        f"🔗 <b>Username:</b> {username}\n"
        f"🆔 <b>Telegram ID:</b> "
        f"<code>{user_id}</code>\n\n"

        f"📂 <b>Категория:</b> {category}\n"
        f"📌 <b>Услуга:</b> {service_name}\n\n"

        f"💬 <b>Сообщение клиента:</b>\n"
        f"{message.text}"
    )

    try:

        await bot.send_message(
            ADMIN_ID,
            admin_text,
            parse_mode="HTML"
        )

        # -------------------------------------------------
        # Ответ клиенту
        # -------------------------------------------------

        await message.answer(
            "✅ Спасибо!\n\n"
            "Ваша заявка отправлена менеджеру.\n"
            "Он ознакомится с ней и свяжется с вами "
            "для уточнения деталей."
        )

        # Удаляем состояние заказа
        del user_orders[user_id]

    except Exception as error:

        print(
            "Ошибка отправки заявки менеджеру:",
            error
        )

        await message.answer(
            "❌ Не удалось отправить заявку менеджеру.\n\n"
            "Попробуйте ещё раз немного позже."
        )


# =========================================================
# ЗАПУСК
# =========================================================

if __name__ == "__main__":

    print("======================================")
    print("      БОТ УСПЕШНО ЗАПУЩЕН")
    print("      AIROGRAM 2.25.1")
    print("======================================")

    executor.start_polling(
        dp,
        skip_updates=True
    )

