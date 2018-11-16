# coding=utf-8
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import config
updater = Updater(token=config.telegram_key)
dispatcher = updater.dispatcher

chatbot = ChatBot(
    'Immortal yet unintellectual'
)

# Create a new trainer for the chatbot
chatbot.set_trainer(ChatterBotCorpusTrainer)

# Train the chatbot based on the english corpus
chatbot.train("chatterbot.corpus.english")

def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Here I am, speaking from the great Eternity')


def textMessage(bot, update):
    response = chatbot.get_response(update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text=str(response))


start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)

dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)

updater.start_polling(clean=True)
updater.idle()
