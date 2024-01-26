import json
import os
import re

# 路径配置
keywords_file_path = 'keywords.json'
commands_file_path = 'commands.json'
pattern = "测试 "  # 你可以根据需要更改这个模式

def load_json(file_path):
    """加载JSON文件，如果文件不存在则返回空字典."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_json(data, file_path):
    """将数据保存到JSON文件。"""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)  # 缩进2个空格

def update_commands(pattern):
    # 加载关键词文件
    keywords_data = load_json(keywords_file_path)
    
    # 初始化commands_data结构
    commands_data = {"name": "keyword_reply", "commands": []}

    # 根据模式提取关键词
    pattern_regex = re.compile("^" + pattern + ".*$")
    for value in keywords_data.values():
        if isinstance(value, list):
            # 如果值是列表，则检查列表中的每个项
            for item in value:
                if pattern_regex.match(item) or not pattern in item:
                    commands_data['commands'].append(item)
        elif isinstance(value, str):
            # 如果值是字符串，检查是否匹配模式或者是否不包含特定模式
            if pattern_regex.match(value) or not pattern in value:
                commands_data['commands'].append(value)

    # 保存更新后的commands.json，此时commands.json会被重写而不是追加内容
    save_json(commands_data, commands_file_path)

# 运行更新命令
update_commands(pattern)
