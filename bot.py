# coding=utf-8
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from parlai.core.params import ParlaiParser
from parlai.core.agents import create_agent
from parlai.core.worlds import create_task
from parlai.core.build_data import download_models
import config

parser = ParlaiParser()
parser.set_params(
        task='backend.talking_agent:TelegramAgent',
        model='projects.personachat.kvmemnn.kvmemnn:KvmemnnAgent',
        model_file='models:personachat/kvmemnn/kvmemnn/persona-self_rephraseTrn-True_rephraseTst-False_lr-0.1_esz-500_margin-0.1_tfidf-False_shareEmb-True_hops1_lins0_model',
        interactive_mode=True,
    )

fnames = ['kvmemnn.tgz']
opt = parser.parse_args()
opt['model_type'] = 'kvmemnn' # for builder
download_models(opt, fnames, 'personachat')

updater = Updater(token=config.telegram_key)
dispatcher = updater.dispatcher

opt['bot'] = updater.bot

# Create model and assign it to the specified task
agent = create_agent(opt, requireModelExists=True)
world = create_task(opt, agent)

def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Here I am, speaking from the great Eternity')


def textMessage(bot, update):
    agent.add_message(update)
    world.parley()


start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)

dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)

updater.start_polling(clean=True)
updater.idle()
