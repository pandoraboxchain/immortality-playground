#!/usr/bin/env python3

from parlai.core.agents import Agent
from parlai.core.utils import display_messages, load_cands


class TelegramAgent(Agent):

    message_queue = []

    def __init__(self, opt, shared=None):
        super().__init__(opt)
        self.id = 'Telegram'
        self.episodeDone = False
        self.bot = opt['bot']


    def observe(self, msg):
        current_message = TelegramAgent.message_queue.pop()
        self.bot.send_message(chat_id=current_message.chat_id,
                              text=display_messages([msg], prettify=True, ignore_fields='text_candidates'))

    def add_message(self, update):
        TelegramAgent.message_queue.insert(0, update.message)

    def act(self):
        reply = {}
        reply['id'] = self.getID()
        current_message = TelegramAgent.message_queue[-1];
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
        return self.episodeDone
