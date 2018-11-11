import requests
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

updater = Updater(token="570424499:AAGtsWf7uA_0BmbLyr5WDEE-7VT0mgh8biw")
dispatcher = updater.dispatcher

print("Bot is alive")


def get_answer(text):
    url = "https://94d914e9.ngrok.io/send_message"
    response_text = {"message": text}
    print("LOG[JSON.QUERY]: " + str(json.dumps(response_text)))
    question = requests.post(url=url, data=response_text)
    response = question.json()
    print("LOG[JSON.RESPONSE]: " + str(response) + " " + question + "\n")
    return response['message']


def text_message(bot, update):
    message = update.message
    chat_id = update.message.chat_id
    temp_text = str(message.text).lower()
    answer = get_answer(temp_text)

    # {"Type": "film","Title" : " Титаник " ,"Released" : " 1997-11-18 ","Video":youtubelink,"Poster": urlpng,"Tagline":"Ничто на Земле не сможет разлучить их.","Score":"7.7","Status":"true"}

    if answer["Type"] == "film":
        bot.send_message(chat_id=chat_id, text="Title: " + answer["Title"] + "\n" +
                                               "Released:" + answer["Released"] + "\n")
    else:
        bot.send_message(chat_id=chat_id, text=answer)


def start_command(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text='Привет! Чем могу помочь?')


start_command_handler = CommandHandler('start', start_command)
text_message_handler = MessageHandler(Filters.text, text_message)

dispatcher.add_handler(text_message_handler)
dispatcher.add_handler(start_command_handler)

updater.start_polling(clean=True)
