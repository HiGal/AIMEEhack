import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import time

import requests
import json


updater = Updater(token='570424499:AAGUvT9EIzpFMZAaxX18q5T-rygcUZJaNDw')
dispatcher = updater.dispatcher

print("Bot is alive")


def get_answer(text):
    url = "https://94d914e9.ngrok.io/send_message"
    response_text = {'message': text}
    print(json.dumps(response_text))
    question = requests.post(url=url, data=response_text)
    print(question)
    response = question.json()
    print(response)
    return str(response)


def text_message(bot, update):
    message = update.message
    temp_text = str(message.text).lower()
    answer = get_answer(temp_text)

    if answer is not None:
        bot.send_message(chat_id=message.chat_id, text=answer)
    else:
        bot.send_message(chat_id=message.chat_id, text='Ответ не распознан. Пожалуйста, перефразируйте.')


def start_command(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text='Привет! Чем могу помочь?')
    time.sleep(1)


# def insertCommand(bot, update):
#     text = update.message.text
#     text_blocks = str(text).split("\n")
#     if len(text_blocks) >= 4:
#         sdk.send_data(text_blocks[1], text_blocks[2], 'id1')
#         db_contexts.insert({'answer': text_blocks[2], 'context': text_blocks[3]})


# def suggestion_command(bot, update):
#     text = update.message.text
#     text_blocks = str(text).split("\n")
#     if len(text_blocks) >= 2:
#         bot.send_message(chat_id=update.message.chat_id, text=str(sdk.get_suggestions(text_blocks[1])))


# def kasko_info(bot, update):
#     keyboard = [[InlineKeyboardButton('Инфо', url='https://goo.gl/bbihY9')]]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     update.message.reply_text('Информация о КАСКО', reply_markup=reply_markup)


# def location(bot, update):
#     bot.send_message(chat_id=update.message.chat_id, text="Вот несколько наших автосалонов")
#     bot.send_message(chat_id=update.message.chat_id, text="Московская ул., 20, Казань, Респ. Татарстан, 420111")
#     bot.send_location(chat_id=update.message.chat_id, latitude=55.7906596, longitude=49.1052328, live_period=80)
#     bot.send_message(chat_id=update.message.chat_id, text="Казань, Респ. Татарстан, 420061")
#     bot.send_location(chat_id=update.message.chat_id, latitude=55.7967087, longitude=49.1912644, live_period=80)
#     bot.send_message(chat_id=update.message.chat_id, text="ул. Габдуллы Тукая, 115 корпус 3, Казань, Респ. Татарстан")
#     bot.send_location(chat_id=update.message.chat_id, latitude=55.766002, longitude=49.1269089, live_period=80)

start_command_handler = CommandHandler('start', start_command)
# insert_command_handler = CommandHandler('insert', insertCommand)
# suggestion_command_handler = CommandHandler('suggestion', suggestion_command)

text_message_handler = MessageHandler(Filters.text, text_message)

dispatcher.add_handler(text_message_handler)
dispatcher.add_handler(start_command_handler)
# dispatcher.add_handler(insert_command_handler)
# dispatcher.add_handler(suggestion_command_handler)

updater.start_polling(clean=True)
