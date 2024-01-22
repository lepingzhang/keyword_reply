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
        for keyword, response in self.keyword_responses.items():
            # 使用正则表达式确保关键词完整匹配（\b表示单词边界）
            if re.search(r'\b' + re.escape(keyword) + r'\b', msg):
                image_url_match = re.search(r'https?://[^\s]+(?:jpg|jpeg|png|gif)', response)
                video_url_match = re.search(r'https?://[^\s]+(?:mp4|avi|mov)', response)

                text_part = re.sub(r'https?://[^\s]+(?:jpg|jpeg|png|gif|mp4|avi|mov)', '', response).strip()

                if text_part and (image_url_match or video_url_match):
                    text_reply = Reply(ReplyType.TEXT, text_part)
                    event.channel.send(text_reply, event.message)

                    media_url = image_url_match.group() if image_url_match else video_url_match.group()
                    media_reply_type = ReplyType.IMAGE if image_url_match else ReplyType.VIDEO
                    media_reply = Reply(media_reply_type, media_url)
                    event.channel.send(media_reply, event.message)
                    event.bypass()

                elif image_url_match:
                    image_reply = Reply(ReplyType.IMAGE, image_url_match.group())
                    event.reply = image_reply
                    event.bypass()

                elif video_url_match:
                    video_reply = Reply(ReplyType.VIDEO, video_url_match.group())
                    event.reply = video_reply
                    event.bypass()

                elif text_part:
                    text_reply = Reply(ReplyType.TEXT, text_part)
                    event.reply = text_reply
                    event.bypass()
                break  # 找到匹配的关键词后即可停止搜索

    def is_image_url(self, url: str) -> bool:
        return re.match(r'https?://[^\s]+(?:jpg|jpeg|png|gif)', url) is not None

    def is_video_url(self, url: str) -> bool:
        return re.match(r'https?://[^\s]+(?:mp4|avi|mov)', url) is not None

    def will_generate_reply(self, event: Event):
        pass

    def will_decorate_reply(self, event: Event):
        pass

    def will_send_reply(self, event: Event):
        pass

    def help(self, **kwargs) -> str:
        return "使用 #keyword_reply 命令来激活这个插件，并回复设定的关键词相关信息。"
