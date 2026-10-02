import telebot
from telebot import types
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Получаем токен из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Токен бота не найден. Проверьте файл .env")

bot = telebot.TeleBot(BOT_TOKEN)


# --- Клавиатуры ---
def get_group_selection_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("1 группа", callback_data="group_1"),
        types.InlineKeyboardButton("2 группа", callback_data="group_2"),
    )
    return markup


def get_week_keyboard(group_prefix):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Нечётная неделя", callback_data=f"{group_prefix}_odd"),
        types.InlineKeyboardButton("Чётная неделя", callback_data=f"{group_prefix}_even"),
    )
    markup.add(types.InlineKeyboardButton("Назад к выбору группы", callback_data=f"{group_prefix}_back"))
    return markup


def get_days_keyboard(prefix):
    markup = types.InlineKeyboardMarkup()
    days = [
        ("Понедельник", f"{prefix}_mon"),
        ("Вторник", f"{prefix}_tue"),
        ("Среда", f"{prefix}_wed"),
        ("Четверг", f"{prefix}_thu"),
        ("Пятница", f"{prefix}_fri"),
        ("Суббота", f"{prefix}_sat"),
        ("Воскресенье", f"{prefix}_sun"),
    ]
    for i in range(0, len(days), 2):
        row = [types.InlineKeyboardButton(text=t, callback_data=d) for t, d in days[i:i + 2]]
        markup.add(*row)
    group = prefix.split("_")
    markup.add(types.InlineKeyboardButton("Назад к выбору недели", callback_data=f"{group}_wback"))
    return markup


# --- Расписание (без аудиторий и ФИО преподавателей) ---
SCHEDULE = {
    # ===== ГРУППА 1 — НЕЧЁТНАЯ НЕДЕЛЯ =====
    "g1_odd_mon": (
        "📅 Понедельник (нечётная)\n\n"
        "Выходной"
    ),
    "g1_odd_tue": (
        "📅 Вторник (нечётная)\n\n"
        "Выходной"
    ),
    "g1_odd_wed": (
        "📅 Среда (нечётная)\n\n"
        "1. 8:45–10:15 \nБезопасность жизнедеятельности (Пр)\n"
        "2. 10:25–11:55 \nФизическая культура (Пр)\n"
        "3. 12:05–14:20 \nОперат.сист.и среды (Лек)\n"
        "4. 14:30–16:00 ТОЛЬКО 2 ПДГ!\nМДК 01.01 Техн.разр.прогр.обесп. (Пр)\n"
        "5. 16:10–17:40 ТОЛЬКО 2 ПДГ!\nИнформ. технолог. (Пр)"
    ),
    "g1_odd_thu": (
        "📅 Четверг (нечётная)\n\n"
        "1. 8:45–10:15 КО ВТОРОЙ ПАРЕ\n"
        "2. 10:25–11:55 ТОЛЬКО 1 ПДГ!\nМДК 01.01 Техн.разр.прогр.обесп.\n"
        "3. 12:05–14:20 ТОЛЬКО 1 ПДГ!\nМДК.01.02 Инстр.средств. разработки ПО\n"
        "4. 14:30–16:00 \nОсновы алгоритмизации и программирования (Лек)\n"
        "5. 16:10–17:40 \nИнформ. технолог"
    ),
    "g1_odd_fri": (
        "📅 Пятница (нечётная)\n\n"
        "1. 8:45–10:15 \nОсн.филос. (Лек)\n"
        "2. 10:25–11:55 \nОсн.филос. (Пр)\n"
        "3. 12:05–14:20 \nИстория (Лек)\n"
        "4. 14:30–16:00 \nБезопасность жизнедеятельности (Лек)\n"
        "5. 16:10–17:40 ТОЛЬКО 1 ПДГ!\nИнформ. технолог. (Пр)"
    ),
    "g1_odd_sat": (
        "📅 Суббота (нечётная)\n\n"
        "1. 8:45–10:15 пока уточнается\n"
        "2. 10:25–11:55 пока уточнается"
    ),
    "g1_odd_sun": "📅 Воскресенье (нечётная)\n\nВыходной",

    # ===== ГРУППА 1 — ЧЁТНАЯ НЕДЕЛЯ =====
    "g1_even_mon": (
        "📅 Понедельник (чётная)\n\n"
        "1. 8:45–10:15 ТОЛЬКО 1ПДГ!\nМДК.01.02 Инстр.средств. разработки ПО (Пр)\n"
        "2. 10:25–11:55 \nМДК.01.02 Инстр.средств. разработки ПО (Лек)\n"
        "3. 12:05–14:20 ТОЛЬКО 2 ПДГ!\nМДК.01.02 Инстр.средств. разработки ПО (Пр)\n"
        "4. 14:30–16:00 ТОЛЬКО 2 ПДГ!\nМДК.01.02 Инстр.средств. разработки ПО (Пр)"
    ),
    "g1_even_tue": (
        "📅 Вторник (чётная)\n\n"
        "1. 8:45–10:15 \nПДГ.1: Информ. технолог. (Пр)\nПДГ.2: МДК.01.02 Инстр.средств. разработки ПО (Пр)\n"
        "2. 10:25–11:55 \nПДГ.1: МДК 01.01 Техн.разр.прогр.обесп. (Пр)\nПДГ.2: МДК.01.02 Инстр.средств. разработки ПО (Пр)\n"
        "3. 12:05–14:20 \nМДК 01.01 Техн.разр.прогр.обесп. (Лек)\n"
        "4. 14:30–16:00 ТОЛЬКО 1 ПДГ!\nИнформ. технолог. (Пр)\n"
        "5. 16:10–17:40 ТОЛЬКО 1 ПДГ!\nМДК 01.01 Техн.разр.прогр.обесп. (Пр)"
    ),
    "g1_even_wed": (
        "📅 Среда (чётная)\n\n"
        "1. 8:45–10:15 \nОперат.сист.и среды (Лек)\n"
        "2. 10:25–11:55 \nФизическая культура (Пр)\n"
        "3. 12:05–14:20 \nБезопасность жизнедеятельности (Пр)\n"
        "4. 14:30–16:00 \nИн.яз. в проф.деят-ти (англ.) (Пр)\n"
        "5. 16:10–17:40 \nИнформ. технолог. (Лек)"
    ),
    "g1_even_thu": (
        "📅 Четверг (чётная)\n\n"
        "Выходной"
    ),
    "g1_even_fri": (
        "📅 Пятница (чётная)\n\n"
        "1. 8:45–10:15 \nЭлемен.высш.матем. (Пр)\n"
        "2. 10:25–11:55 \nОсн.филос. (Лек)\n"
        "3. 12:05–14:20 \nИстория (Пр)\n"
        "4. 14:30–16:00 \nЭлемен.высш.матем. (Лек)\n"
        "5. 16:10–17:40 \nИн.яз. в проф.деят-ти (англ.) (Пр)"
    ),
    "g1_even_sat": (
        "📅 Суббота (чётная)\n\n"
        "1. 8:45–10:15 пока уточнается\n"
        "2. 10:25–11:55 пока уточнается"
    ),
    "g1_even_sun": "📅 Воскресенье (чётная)\n\nВыходной",
}


# --- Обработчики команд ---
@bot.message_handler(commands=["start"])
def inline_menu(message):
    bot.send_message(
        message.chat.id,
        "Какая ты группа:",
        reply_markup=get_group_selection_keyboard(),
    )


# --- Обработка нажатий ---
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data in ("group_1", "group_2"):
        group_prefix = "g1" if call.data == "group_1" else "g2"
        group_name = "1" if call.data == "group_1" else "2"
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            f"Вы выбрали {group_name} группу. Выберите неделю:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=get_week_keyboard(group_prefix),
        )

    elif call.data in ("g1_odd", "g1_even", "g2_odd", "g2_even"):
        bot.answer_callback_query(call.id)
        week_type = "нечётная" if "odd" in call.data else "чётная"
        group_name = "1" if "g1" in call.data else "2"
        bot.edit_message_text(
            f"Группа {group_name}, {week_type} неделя. Выберите день:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=get_days_keyboard(call.data),
        )

    elif call.data.endswith("_wback"):
        bot.answer_callback_query(call.id)
        group_prefix = call.data.split("_")
        bot.edit_message_text(
            f"Выберите неделю для группы {'1' if group_prefix == 'g1' else '2'}:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=get_week_keyboard(group_prefix),
        )

    elif call.data.endswith("_back"):
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            "Какая ты группа:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=get_group_selection_keyboard(),
        )

    else:
        text = SCHEDULE.get(call.data, "Расписание пока не задано.")
        bot.answer_callback_query(call.id)
        prefix = call.data.rsplit("_", 1)
        bot.edit_message_text(
            text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=get_days_keyboard(prefix),
        )


# --- Запуск ---
if __name__ == "__main__":
    print("Бот успешно запущен и слушает команды...")
    bot.infinity_polling()
