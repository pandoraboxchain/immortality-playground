#!/usr/bin/env python3

from parlai.core.agents import Agent
from parlai.core.utils import display_messages, load_cands


class TelegramAgent(Agent):

    def __init__(self, opt, shared=None):
        super().__init__(opt)
        self.id = 'Telegram'
        self.episodeDone = False
        self.message_queue = []
        self.seen_messages = {}
        self.bot = opt['bot']

    def observe(self, msg):
        current_message = self.message_queue.pop(0)
        self.bot.send_message(chat_id=current_message.chat_id,
                              text=display_messages([msg], prettify=self.opt.get('display_prettify', True)))
        print(display_messages([msg],
                               ignore_fields=self.opt.get('display_ignore_fields', ''),
                               prettify=self.opt.get('display_prettify', True)))

    def add_message(self, update):
       self.message_queue.insert(0, update.message)

    def act(self):
        reply = {}
        reply['id'] = self.getID()
        current_message = self.message_queue[0];
        reply_text = current_message.text
        reply_text = reply_text.replace('\\n', '\n')
        reply['episode_done'] = False
        if '[DONE]' in reply_text:
            reply['episode_done'] = True
            self.episodeDone = True
            reply_text = reply_text.replace('[DONE]', '')
        reply['text'] = reply_text
        return reply

    def episode_done(self):
        self.chat_id = 0
        return self.episodeDone
