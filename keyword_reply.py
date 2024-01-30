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
            msg = re.sub(r'@[\w]+\s+', '', msg, count=1).strip()

        for keyword, response in self.keyword_responses.items():
            if re.search(r'\b' + re.escape(keyword) + r'\b', msg):
                image_url_match = re.search(r'https?://[^\s]+(?:jpg|jpeg|png|gif)', response)
                video_url_match = re.search(r'https?://[^\s]+(?:mp4|avi|mov)', response)

                text_part = re.sub(r'https?://[^\s]+(?:jpg|jpeg|png|gif|mp4|avi|mov)', '', response).strip()

                if text_part:
                    text_reply = Reply(ReplyType.TEXT, text_part)
                    event.channel.send(text_reply, event.message)

                if image_url_match:
                    image_reply = Reply(ReplyType.IMAGE, image_url_match.group())
                    event.channel.send(image_reply, event.message)

                if video_url_match:
                    video_reply = Reply(ReplyType.VIDEO, video_url_match.group())
                    event.channel.send(video_reply, event.message)

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
