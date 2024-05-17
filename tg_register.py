from constants import BOT_TOKEN
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.async_telebot import AsyncTeleBot
from register_mail import RegisterBot

# regbot = RegisterBot()

bot = AsyncTeleBot(BOT_TOKEN)

users = {}


@bot.message_handler(commands=['start'])
async def start_message(message):
    # keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    # button_support = KeyboardButton(text="Решить капчу")
    # keyboard.add(button_support)
    if message.chat.id not in users:
        users[message.chat.id] = {'bot': RegisterBot()}
    # await bot.send_message(message.chat.id, 'Теперь вы в системе Бота.\n Для прохождения капчи введите `Решить капчу`',
    #                  reply_markup=keyboard)
    regbot = users[message.chat.id]['bot']
    regbot.register_mail()
    if regbot.current_captcha['task'] is not None:
        await bot.send_message(message.chat.id, regbot.person)
        await bot.send_message(message.chat.id, "Введите капчу для создания почты")
        await bot.send_photo(message.chat.id, regbot.current_captcha['task'])


@bot.message_handler(func=lambda message: message.text == 'Решить капчу')
async def solve_captcha(message):
    if users[message.chat.id]['bot'].current_captcha['task'] is not None:
        await bot.send_message(message.chat.id, users[message.chat.id]['bot'].person)
        await bot.send_photo(message.chat.id, users[message.chat.id]['bot'].current_captcha['task'])
        # bot.register_next_step_handler(message, save_solve)
    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        button_support = KeyboardButton(text="Решить капчу")
        keyboard.add(button_support)
        await bot.send_message(message.chat.id, 'Пока для вас нет капч(',
                               reply_markup=keyboard)


@bot.message_handler(func=lambda message: len(message.text) == 6)
async def save_solve(message):
    regbot = users[message.chat.id]['bot']
    regbot.current_captcha['solve'] = message.text.strip()
    regbot.solve_captcha()

    regbot.current_captcha['solve'] = None
    regbot.current_captcha['task'] = None

    regbot.driver.quit()
    regbot._init_driver()

    await regbot.register_mail()
    if regbot.current_captcha['task'] is not None:
        await bot.send_message(message.chat.id, regbot.person)
        await bot.send_message(message.chat.id, "Введите капчу для создания почты")
        await bot.send_photo(message.chat.id, regbot.current_captcha['task'])


import asyncio

asyncio.run(bot.polling(non_stop=True, request_timeout=180))
