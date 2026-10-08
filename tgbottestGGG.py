import random
import telebot

TOKEN = "8922413193:AAGsdLoId3VpvCZK8PVCY6L4YDrr-5g_Vmo"

bot = telebot.TeleBot(TOKEN)

games = {}


@bot.message_handler(commands=["start"])
def start(message):
    games[message.chat.id] = {"number": random.randint(1, 100), "attempts": 0}

    bot.send_message(
        message.chat.id,
        "🎮 Игра «Угадай число» — версия 3!"
        "Я загадал число от 1 до 100.\n"
        "Попробуй угадать его!",
    )


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


@bot.message_handler(func=lambda message: True)
def guess(message):
    chat_id = message.chat.id

    if chat_id not in games:
        bot.send_message(chat_id, "Сначала напиши /start")
        return

    try:
        number = int(message.text)
    except ValueError:
        bot.send_message(chat_id, "❌ Напиши число.")
        return

    secret = games[chat_id]["number"]
    games[chat_id]["attempts"] += 1

    if number < secret:
        bot.send_message(chat_id, "⬆️ Моё число больше!")

    elif number > secret:
        bot.send_message(chat_id, "⬇️ Моё число меньше!")

    else:
        attempts = games[chat_id]["attempts"]

    bot.send_message(
        chat_id,
        f"🎉 Правильно! Я загадал число {secret}.\n"
        f"🔢 Количество попыток: {attempts}\n\n"
        "Напиши /start, чтобы сыграть ещё раз.",
    )

    del games[chat_id]


print("Бот запущен...")
bot.infinity_polling()
