import requests
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


TELEGRAM_API_TOKEN = "570424499:AAGtsWf7uA_0BmbLyr5WDEE-7VT0mgh8biw"
updater = Updater(token=TELEGRAM_API_TOKEN)
dispatcher = updater.dispatcher

print("Bot is alive")


def get_answer(text):
    url = "https://94d914e9.ngrok.io/send_message"
    response_text = {"message": text}
    print("LOG[JSON.QUERY]: " + str(json.dumps(response_text)))
    question = requests.post(url=url, data=response_text)
    response = question.json()
    print("LOG[JSON.RESPONSE]: " + str(response) + " " + str(question) + "\n")
    return response['message']


def text_message(bot, update):
    message = update.message
    chat_id = update.message.chat_id
    temp_text = str(message.text).lower()
    answer = get_answer(temp_text)

    # {"Type": "film","Title" : " Титаник " ,"Released" : " 1997-11-18 ","Video":youtubelink,"Poster": urlpng,"Tagline":"Ничто на Земле не сможет разлучить их.","Score":"7.7","Status":"true"}

    if answer["Type"] == "film":
        bot.send_message(chat_id    =chat_id, text="Title: " + answer["Title"] + "\n" +
                                               "Released:" + answer["Released"] + "\n")
    else:
        bot.send_message(chat_id=chat_id, text=answer)


def voice_message(bot, update):
    message = update.message
    chat_id = message.chat_id
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get(file_info.file_path)

    url = "https://94d914e9.ngrok.io/detect_voice"
    response_text = {file.content}
    question = requests.post(url=url, data=response_text)
    response = question.json()
    print("LOG[JSON.RESPONSE]: " + str(response) + " " + str(question) + "\n")
    bot.send_message(chat_id=chat_id, text="voice блять")


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
