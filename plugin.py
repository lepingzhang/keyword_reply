import os
import json
import re
from plugins import register, Plugin, Event, Reply, ReplyType

@register
class SimpleKeywordReplyBot(Plugin):
    name = 'keyword_reply'

    def __init__(self, config: dict):
        super().__init__(config)
        self.keyword_responses = self.load_keywords()

    def load_keywords(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(dir, 'keywords.json')
        try:
            with open(path, mode='r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as exc:
            print(f'Failed to load keywords: {exc}')
            return {}

    def did_receive_message(self, event: Event):
        msg = event.message.content
        for keyword, response in self.keyword_responses.items():
            if keyword in msg:
                # 使用正则表达式匹配图片和视频链接
                image_url_match = re.search(r'https?://[^\s]+(?:jpg|jpeg|png|gif)', response)
                video_url_match = re.search(r'https?://[^\s]+(?:mp4|avi|mov)', response)

                # 分离文本和媒体链接
                text_part = response
                if image_url_match or video_url_match:
                    text_part = re.sub(r'https?://[^\s]+(?:jpg|jpeg|png|gif|mp4|avi|mov)', '', response).strip()

                # 检查是否同时存在文本和媒体链接
                if (text_part and (image_url_match or video_url_match)):
                    # 合并文本和媒体链接为一个文本回复
                    media_url = image_url_match.group() if image_url_match else video_url_match.group()
                    compound_reply = f"{text_part}\n{media_url}"
                    event.reply = Reply(ReplyType.TEXT, compound_reply)
                    event.bypass()
                elif image_url_match:
                    # 仅有图片链接
                    image_reply = Reply(ReplyType.IMAGE, image_url_match.group())
                    event.reply = image_reply
                    event.bypass()
                elif video_url_match:
                    # 仅有视频链接
                    video_reply = Reply(ReplyType.VIDEO, video_url_match.group())
                    event.reply = video_reply
                    event.bypass()
                elif text_part:
                    # 仅有文本
                    text_reply = Reply(ReplyType.TEXT, text_part)
                    event.reply = text_reply
                    event.bypass()
                break

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
