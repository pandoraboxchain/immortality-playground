# coding=utf-8
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from parlai.core.params import ParlaiParser
from parlai.core.agents import create_agent
from parlai.core.worlds import create_task
from parlai.core.build_data import download_models
from projects.personachat.persona_seq2seq import PersonachatSeqseqAgentSplit
import config

parser = ParlaiParser(add_model_args=True)
parser.add_argument('-d', '--display-examples', type='bool', default=False)
PersonachatSeqseqAgentSplit.add_cmdline_args(parser)
parser.set_defaults(
    dict_file='models:personachat/profile_memory/fulldict.dict',
    interactive_mode=True,
    task='backend.talking_agent:TelegramAgent',
    model='projects.personachat.persona_seq2seq:PersonachatSeqseqAgentSplit',
    model_file='models:personachat/profile_memory/profilememory_learnreweight_sharelt_encdropout0.4_s2s_usepersona_self_useall_attn_general_lstm_1024_1_1e-3_0.1'
)

opt = parser.parse_args()
opt['model_type'] = 'profile_memory'

fnames = ['profilememory_mem2_reweight_sharelt_encdropout0.2_selfpersona_useall_attn_general_lstm_1024_1_1e-3_0.1',
          'profilememory_learnreweight_sharelt_encdropout0.4_s2s_usepersona_self_useall_attn_general_lstm_1024_1_1e-3_0.1',
          'fulldict.dict']
download_models(opt, fnames, 'personachat')

updater = Updater(token=config.telegram_key)
dispatcher = updater.dispatcher

opt['bot'] = updater.bot

# Create model and assign it to the specified task
agent = create_agent(opt, requireModelExists=False) 
world = create_task(opt, agent)

def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Here I am, speaking from the great Eternity')


def textMessage(bot, update):
    # FIXME find a better way to pass the chat without encapsulation violation
    world.agents[0].add_message(update)
    world.parley()


start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)

dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)

updater.start_polling(clean=True)
updater.idle()
