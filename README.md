# wechat-gptbot关键字回复插件

本项目作为 `wechat-gptbot` 插件，可以根据关键字回复对应的信息。

## 安装指南

### 1. 添加插件源
在 `plugins/source.json` 文件中添加以下配置：

```json
{
  "keyword_reply": {
    "repo": "https://github.com/lepingzhang/keyword_reply.git",
    "desc": "关键字回复"
  }
}

2. 插件配置
在 config.json 文件中添加以下配置：
{
  "name": "keyword_reply",
  "commands": [
    "hello",
    "bye",
    "help"
  ]
}

鸣谢
感谢以下项目对本插件的支持和启发：

wechat-douyin-scraper: 一个高效的微信及抖音数据抓取工具。
