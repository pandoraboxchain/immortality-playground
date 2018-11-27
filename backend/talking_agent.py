#!/usr/bin/env python3

from parlai.core.agents import Agent
from parlai.core.utils import display_messages


class TelegramAgent(Agent):

    message_queue = []

    def __init__(self, opt, shared=None):
        super().__init__(opt)
        self.id = 'Telegram'
        self.episodeDone = False
        self.bot = opt['bot']


    def observe(self, msg):
        current_message = TelegramAgent.message_queue.pop()
        msg_text = display_messages(text=display_messages([msg], prettify=True, ignore_fields='text_candidates'))
        self.bot.send_message(chat_id=current_message.chat_id,
                              text=msg_text.replace("[Seq2Seq]:", ""))

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
