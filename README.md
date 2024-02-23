# wechat-gptbot 关键字回复插件

本项目作为 `wechat-gptbot` 插件，可以根据关键字回复对应的信息。

## 安装指南

### 1、添加插件源
在 `plugins/source.json` 文件中添加以下配置：
```
{
  "keyword_reply": {
    "repo": "https://github.com/lepingzhang/keyword_reply.git",
    "desc": "关键字回复"
  }
}
```

### 2、插件配置
在 `config.json` 文件中添加以下配置：
```
{
  "plugins": [
    {
      "name": "keyword_reply"
    }
  ]
}
```

### 3、关键词添加和导出
3-1：在`keywords.json`中添加关键词以及对应的回复内容；
3-2: `keywords.json`可以单独更新而无需重启插件。

~~3-2：运行`output_commends_clear.py`即可得到`commands.json`；~~

~~3-3：将里面的关键词复制粘贴到`config.json`对应位置即可~~

### 鸣谢
感恩[wechat-douyin-scraper](https://github.com/al-one/wechat-douyin-scraper)项目对本插件的支持和启发。
