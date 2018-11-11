import requests
import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TELEGRAM_API_TOKEN = "768912317:AAEp51lJL9IniuEVEtjjZRShJBreVSXz2f8"
NGROK = "https://7b68ccdb.ngrok.io"

updater = Updater(token=TELEGRAM_API_TOKEN)
dispatcher = updater.dispatcher

print("Bot is alive")


def get_answer(text) -> str:
    url = NGROK + "/send_message"
    response_text = {"message": text}
    print("LOG[JSON.QUERY]: " + str(json.dumps(response_text)))
    question = requests.post(url=url, data=response_text)
    response = question.json()
    print("LOG[JSON.RESPONSE]: " + str(response) + " " + str(question) + "\n")
    return response['message']


def json_string_to_dict(text: str) -> dict:
    text_entities = text.strip('{}').split(",")
    string_dict = {}
    for i in text_entities:
        temp = i.split(":")
        string_dict.update({temp[0].lstrip(" \"").rstrip("\" "): temp[1].strip().lstrip(" \"").rstrip("\" ")})
    return string_dict


def text_message(bot, update):
    message = update.message

    temp_text = str(message.text).lower()
    answer = get_answer(temp_text)
    responseView(bot, update, answer)


def responseView(bot, update, answer: str):
    chat_id = update.message.chat_id
    if not answer.find("Type") == -1:
        answer_dict = json.loads(answer)
        if answer_dict["Type"] == "film":
            film_description = ("Фильм: <b>" + answer_dict["Title"].lstrip().rstrip() + "</b>\n" +
                                "Дата релиза: " + answer_dict["Released"].replace("-", ".").lstrip().rstrip() + "\n" +
                                "Трейлер: <a href=\"" + answer_dict["Video"] + "\">youtube</a>\n" +
                                "Слоган: <i>" + answer_dict["Tagline"] + "</i>\n" +
                                "Рейтинг: <b>" + answer_dict["Score"] + "</b>\n" +
                                "В прокате: <b>" + answer_dict["Status"].replace("true", "Да").replace("false",
                                                                                                       "Нет") + "</b>\n")
            print(film_description)
            bot.send_photo(chat_id=chat_id, photo=answer_dict["Poster"])
            if answer_dict["Status"] == "true":
                keyboard = [[InlineKeyboardButton('Купить билеты:', url='https://karofilm.ru/theatres/26')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text(film_description, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
            else:
                bot.send_message(chat_id=chat_id, text=film_description, parse_mode=ParseMode.HTML)
        elif answer_dict["Type"] == "location":
            bot.send_message(chat_id=chat_id, text="Вот несколько банкоматов поблизости:")
            bot.send_location(chat_id=chat_id, latitude=55.780311, longitude=49.133646, live_period=80)
            bot.send_location(chat_id=chat_id, latitude=55.779603, longitude=49.135085, live_period=80)
        elif answer_dict["Type"] == "auto":
            bot.send_message(chat_id=chat_id, text="Вот несколько наших автосалонов поблизости")
            bot.send_message(chat_id=chat_id, text="Московская ул., 20, Казань, Респ. Татарстан, 420111")
            bot.send_location(chat_id=chat_id, latitude=55.7906596, longitude=49.1052328, live_period=80)
            bot.send_message(chat_id=chat_id, text="Казань, Респ. Татарстан, 420061")
            bot.send_location(chat_id=chat_id, latitude=55.7967087, longitude=49.1912644, live_period=80)
            bot.send_message(chat_id=chat_id,
                             text="ул. Габдуллы Тукая, 115 корпус 3, Казань, Респ. Татарстан")
            bot.send_location(chat_id=chat_id, latitude=55.766002, longitude=49.1269089, live_period=80)
        elif answer_dict["Type"] == "kasko":
            keyboard = [[InlineKeyboardButton('Форма', url='https://goo.gl/forms/XAQP8XrHb48X7hOv2')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                'Форма для предварительного оформления КАСКО, оставшаяся часть документов будет оформлена в салоне',
                reply_markup=reply_markup)
        elif answer_dict["Type"] == "osago":
            keyboard = [[InlineKeyboardButton('Форма', url='https://goo.gl/forms/iJcFeID1ynYCXow83')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('Форма для оформления ОСАГО', reply_markup=reply_markup)
        elif answer_dict["Type"] == "ticket":
            bot.send_message(chat_id=chat_id, text="Откуда: <i>" + answer_dict["Origin"] + "</i>\n" +
                                                   "Куда: <i>" + answer_dict["Destination"] + "</i>\n" +
                                                   "Цена: <b>" + answer_dict["Price"] + "</b>",
                             parse_mode=ParseMode.HTML)
            insurance = "Вы можете <b>застраховать себя</b> от несчастных случаев, потери багажа и задержки рейса."
            keyboard = [[InlineKeyboardButton("Узнать больше", url='https://sgabs.ru/products/pilgrim.php')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(insurance, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        else:
            bot.send_message(chat_id=chat_id, text=answer_dict)
    else:
        bot.send_message(chat_id=chat_id, text=str(answer))


def voice_message(bot, update):
    message = update.message
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get(file_info.file_path)

    url = NGROK + "/detect_voice"
    question = requests.post(url=url, data=file.content)
    response = question.json()
    responseView(bot, update, response['message'])


def start_command(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text='Привет! Чем могу помочь?')


start_command_handler = CommandHandler('start', start_command)
text_message_handler = MessageHandler(Filters.text, text_message)
voice_message_handler = MessageHandler(Filters.voice, voice_message)

dispatcher.add_handler(text_message_handler)
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(voice_message_handler)

updater.start_polling(clean=True)
