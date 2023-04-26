from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from src.get_best_move import get_best_move, cfg, re

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)
flag = False
current_url = ""

# Warning!!! This file contains some Cyrillic symbols.
# It is important, because the bot is designed for Russian chess players.
# Thank you for understanding.


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This is a welcome message for new user.
    """

    await message.reply("Привет! Я шахматный ассистент Chassh legend."
                        "Я буду помогать тебе учиться играть в шахматы.")


@dp.message_handler(Text(equals='Новая партия'))
async def get_url_new_game(message: types.Message):
    """
    This function finds the best move for user, when he wants to analyze new game.
    """

    await message.answer("Введи ссылку на партию на lichess.org, чтобы я мог найти лучший ход.")

    url = message.text
    global current_url
    current_url = url

    # Checking, if it is a link to the lichess.org game.


@dp.message_handler(Text(contains='lichess.org'))
async def get_move_new_game(message: types.Message):
    global current_url
    if not re.search(r'lichess.org/.*', message.text):
        print(message.text)
        print(current_url)
        await message.answer("Твоя ссылка некорректна."
                             "Пожалуйста, введи ссылку на партию на lichess.org")
        return

    current_url = message.text
    global flag
    flag = True

    try:
        best_move = get_best_move(message.text)
        await message.reply(f"{best_move}")
    except Exception as e:
        await message.reply("К сожалению, произошла ошибка при поиске лучшего хода. "
                            "Пожалуйста, попробуй еще раз.")
        print(e)


@dp.message_handler(Text(equals='Текущая партия'))
async def get_move_current_game(message: types.Message):
    """
    This function finds the best move for user, when he wants to analyze position in current game.
    """

    if not flag:
        await message.reply("Но ты не указывал никакой партии ранее."
                            "Всё пошло не очень хорошо. Давай по новой.")
        return

    try:
        best_move = get_best_move(current_url)
        await message.reply(f"{best_move}")
    except Exception as e:
        await message.reply("К сожалению, произошла ошибка при поиске лучшего хода. "
                            "Пожалуйста, попробуй еще раз.")
        print(e)


@dp.message_handler()
async def start(message: types.Message):
    """
    Default message from the bot.
    """

    start_buttons = ['Новая партия', 'Текущая партия']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Я тебя не понимаю.'
                         'Пожалуйста, сообщи, что бы ты хотел проанализировать?', reply_markup=keyboard)


def main():
    executor.start_polling(dp)  # , skip_updates=True)


if __name__ == '__main__':
    main()
