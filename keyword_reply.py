import os
import json
import re
from plugins import register, Plugin, Event, Reply, ReplyType

@register
class KeywordReply(Plugin):
    name = 'keyword_reply'

    def __init__(self, config: dict):
        super().__init__(config)
        self.keyword_responses = self.load_keywords()

    def load_keywords(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(dir, 'keywords.json')
        keyword_responses = {}
        try:
            with open(path, mode='r', encoding='utf-8') as file:
                responses = json.load(file)
                for response, keywords in responses.items():
                    for keyword in keywords:
                        keyword_responses[keyword] = response
        except Exception as exc:
            print(f'Failed to load keywords: {exc}')
        return keyword_responses

    def did_receive_message(self, event: Event):
        msg = event.message.content
        is_group = event.message.is_group
        is_at = event.message.is_at

        if is_group and is_at:
            # 使用正则表达式分割消息，以处理不同类型的空白字符
            parts = re.split(r'\s+', msg, maxsplit=1)
            if len(parts) > 1:
                msg = parts[1].strip()
            else:
                msg = parts[0].strip()

        for keyword, response in self.keyword_responses.items():
            if re.search(r'\b' + re.escape(keyword) + r'\b', msg):
                text_reply = Reply(ReplyType.TEXT, response)
                event.reply = text_reply
                event.bypass()
                break

    def help(self, **kwargs) -> str:
        return "使用 #keyword_reply 命令来激活这个插件，并回复设定的关键词相关信息。"

    def will_generate_reply(self, event: Event):
        pass

    def will_decorate_reply(self, event: Event):
        pass

    def will_send_reply(self, event: Event):
        pass
