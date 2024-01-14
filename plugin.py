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
                # 使用正则表达式匹配图片链接
                image_urls = re.findall(r'https?://[^\s]+(?:jpg|jpeg|png|gif)', response)
                image_url = image_urls[0] if image_urls else ""

                # 移除图片链接，剩下的部分为文本
                text_part = re.sub(r'https?://[^\s]+(?:jpg|jpeg|png|gif)', '', response).strip()

                # 发送文本部分（如果存在）
                if text_part:
                    text_reply = Reply(ReplyType.TEXT, text_part)
                    event.reply = text_reply
                    event.bypass()

                # 检查并发送图片链接（如果存在）
                if self.is_image_url(image_url):
                    image_reply = Reply(ReplyType.IMAGE, image_url)
                    event.reply = image_reply
                    event.bypass()

                break  # 匹配到关键词后，不再检查其他关键词

    def is_image_url(self, url: str) -> bool:
        # 检查链接是否是图片链接
        return re.match(r'https?://[^\s]+(?:jpg|jpeg|png|gif)', url) is not None

    def will_generate_reply(self, event: Event):
        # 这个方法会在生成回复之前被调用
        pass

    def will_decorate_reply(self, event: Event):
        # 这个方法会在装饰回复之前被调用
        pass

    def will_send_reply(self, event: Event):
        # 这个方法会在发送回复之前被调用
        pass

    def help(self, **kwargs) -> str:
        # 这个方法用于展示插件的帮助文档
        return "使用 #keyword_reply 命令来激活这个插件，并回复设定的关键词相关信息。"
