import random
import telebot
from telebot import types

TOKEN = "ВСТАВЬ_НОВЫЙ_ТОКЕН"

bot = telebot.TeleBot(TOKEN)
games = {}
game_history = {}


def start_game(message):
    chat_id = message.chat.id
    games[chat_id] = {"number": random.randint(1, 100), "attempts": 0}

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        types.KeyboardButton("🎮 Новая игра"), types.KeyboardButton("📜 История")
    )

    bot.send_message(
        chat_id,
        "🎮 Игра «Угадай число» — версия 5!\n"
        "Я загадал число от 1 до 100.\n"
        "Попробуй угадать его!",
        reply_markup=keyboard,
    )


@bot.message_handler(commands=["start"])
def start(message):
    start_game(message)


@bot.message_handler(commands=["hint"])
def hint(message):
    chat_id = message.chat.id

    if chat_id not in games:
        bot.send_message(chat_id, "Сначала начни игру командой /start.")
        return

    secret = games[chat_id]["number"]

    if secret % 2 == 0:
        bot.send_message(chat_id, "💡 Подсказка: моё число — чётное.")
    else:
        bot.send_message(chat_id, "💡 Подсказка: моё число — нечётное.")


@bot.message_handler(func=lambda message: message.text == "🎮 Новая игра")
def new_game(message):
    start_game(message)


@bot.message_handler(func=lambda message: message.text == "📜 История")
def history(message):
    chat_id = message.chat.id
    records = game_history.get(chat_id, [])

    if not records:
        bot.send_message(
            chat_id, "📜 История пока пуста. Сначала сыграй и угадай число!"
        )
        return

    text = "📜 Последние игры:\n\n"

    for i, game in enumerate(reversed(records), 1):
        text += f"{i}. Число: {game['number']} — попыток: {game['attempts']}\n"

    bot.send_message(chat_id, text)


@bot.message_handler(func=lambda message: True)
def guess(message):
    chat_id = message.chat.id

    if chat_id not in games:
        bot.send_message(chat_id, "Сначала напиши /start")
        return

    try:
        number = int(message.text)
    except (ValueError, TypeError):
        bot.send_message(chat_id, "❌ Напиши число.")
        return

    if not 1 <= number <= 100:
        bot.send_message(chat_id, "❌ Введи число от 1 до 100.")
        return

    secret = games[chat_id]["number"]
    games[chat_id]["attempts"] += 1

    if number < secret:
        bot.send_message(chat_id, "⬆️ Моё число больше!")

    elif number > secret:
        bot.send_message(chat_id, "⬇️ Моё число меньше!")

    else:
        attempts = games[chat_id]["attempts"]

        game_history.setdefault(chat_id, []).append(
            {"number": secret, "attempts": attempts}
        )

        game_history[chat_id] = game_history[chat_id][-10:]

        bot.send_message(
            chat_id,
            f"🎉 Правильно! Я загадал число {secret}.\n"
            f"🔢 Количество попыток: {attempts}\n\n"
            "Нажми «🎮 Новая игра», чтобы сыграть ещё раз.",
        )

        del games[chat_id]


print("Бот запущен...")
bot.infinity_polling()
