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
                # 检查回复内容是否为图片链接
                if self.is_image_url(response):
                    # 如果是图片链接，则发送图片回复
                    reply = Reply(ReplyType.IMAGE, response)
                else:
                    # 否则发送文本回复
                    reply = Reply(ReplyType.TEXT, response)
                event.reply = reply
                event.bypass()  # 绕过后续插件处理，直接发送回复
                break  # 匹配到关键词后，不再检查其他关键词

    def is_image_url(self, url: str) -> bool:
        # 检查链接是否以 .jpg, .jpeg, .png, .gif 结尾
        return re.match(r'.*\.(jpg|jpeg|png|gif)$', url, re.IGNORECASE) is not None

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
