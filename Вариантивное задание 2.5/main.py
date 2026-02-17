import telebot
from telebot import types

TOKEN = "ВАШ_ТОКЕН"
bot = telebot.TeleBot(TOKEN)

QUESTIONS = [
    ("Как дела?", ["Отлично", "Нормально", "Не очень"]),
    ("Какая погода нравится больше?", ["Солнечно", "Пасмурно", "Снег"]),
    ("Любимый жанр фильмов?", ["Комедия", "Фантастика", "Боевик"]),
    ("Что выбрать на ужин?", ["Паста", "Пицца", "Салат"]),
    ("Какой язык программирования интересен?", ["Python", "Java", "C++"]),
    ("Что посоветуешь для отдыха?", ["Сон", "Прогулка", "Сериал"]),
    ("Кофе или чай?", ["Кофе", "Чай", "Ни то, ни другое"]),
    ("Учёба сегодня была?", ["Да", "Нет", "Завтра"]),
    ("Любимая музыка?", ["Поп", "Рок", "Электро"]),
    ("Хочешь ещё вопрос?", ["Да", "Нет"])
]

user_step = {}

def make_keyboard(options):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for opt in options:
        kb.add(types.KeyboardButton(opt))
    kb.add(types.KeyboardButton("Следующий вопрос"))
    kb.add(types.KeyboardButton("Старт заново"))
    return kb

@bot.message_handler(commands=["start"])
def start(message):
    user_step[message.chat.id] = 0
    bot.send_message(
        message.chat.id,
        "Привет! Нажми 'Следующий вопрос', чтобы начать.",
        reply_markup=make_keyboard(["Следующий вопрос"])
    )

@bot.message_handler(func=lambda m: True)
def dialog(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if text == "Старт заново":
        user_step[chat_id] = 0
        bot.send_message(chat_id, "Ок, начинаем заново.", reply_markup=make_keyboard(["Следующий вопрос"]))
        return

    if text == "Следующий вопрос":
        step = user_step.get(chat_id, 0)
        if step >= len(QUESTIONS):
            bot.send_message(chat_id, "Вопросы закончились. Нажми 'Старт заново'.", reply_markup=make_keyboard(["Старт заново"]))
            return

        q_text, answers = QUESTIONS[step]
        user_step[chat_id] = step + 1
        bot.send_message(chat_id, q_text, reply_markup=make_keyboard(answers))
        return

    bot.send_message(chat_id, f"Принято: {text}. Нажми 'Следующий вопрос'.")

bot.infinity_polling()
