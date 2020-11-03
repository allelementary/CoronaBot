import telebot
from telebot import types
from covid import Covid

covid = Covid()
bot = telebot.TeleBot('***code ')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Whole World')
    btn2 = types.KeyboardButton('US')
    btn3 = types.KeyboardButton('Russia')
    btn4 = types.KeyboardButton('China')
    btn5 = types.KeyboardButton('List of Countries')
    markup.add(btn1, btn2, btn3, btn4, btn5)

    send_message = f"<b>Привет, {message.from_user.first_name}!</b>\nЧтобы узнать данные о распространении вируса, " \
                   f"напишите название страны на английском, например: US, Russia, Ukraine, и так далее\n"
    bot.send_message(message.chat.id, send_message, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def mess(message):
    get_message_bot = message.text.strip().lower()
    try:
        if get_message_bot == "whole world":
            deaths = covid.get_total_deaths()
            confirmed = covid.get_total_confirmed_cases()
            recovered = covid.get_total_recovered()
            final_message = f"<b>Entire World:</b> \nConfirmed: {confirmed}, \nRecovered: {recovered}, \n" \
                            f"Deaths: {deaths}"

        else:
            country_list = []
            for country in covid.list_countries():
                country_name = country['name']
                if country_name.startswith(get_message_bot[0]):
                    country_list.append(country_name)
            final_message = f'{country_list}'

    except ValueError as exc:
        print(f'Got {exc}')
        final_message = f'<b>There is no country called {get_message_bot}. \n'\
                        'You can check available countries at</b> https://coronavirus.jhu.edu/data/mortality'

    bot.send_message(message.chat.id, final_message, parse_mode='html')


bot.polling(none_stop=True)
