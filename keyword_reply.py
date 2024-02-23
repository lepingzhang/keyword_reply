import os
import json
import re
from plugins import register, Plugin, Event, Reply, ReplyType
import time

@register
class KeywordReply(Plugin):
    name = 'keyword_reply'

    def __init__(self, config: dict):
        super().__init__(config)
        self.keywords_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keywords.json')
        self.keyword_responses = {}
        self.file_last_modified = 0
        self.load_keywords()

    def load_keywords(self):
        try:
            last_modified = os.path.getmtime(self.keywords_file_path)
            if last_modified != self.file_last_modified:
                with open(self.keywords_file_path, mode='r', encoding='utf-8') as file:
                    responses = json.load(file)
                    self.keyword_responses = {keyword: response for response in responses for keyword in responses[response]}
                    self.file_last_modified = last_modified
        except Exception as exc:
            print(f'Failed to load keywords: {exc}')

    def did_receive_message(self, event: Event):
        self.load_keywords()
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
        return "根据关键词回复设定的相关信息"

    def will_generate_reply(self, event: Event):
        pass

    def will_decorate_reply(self, event: Event):
        pass

    def will_send_reply(self, event: Event):
        pass
