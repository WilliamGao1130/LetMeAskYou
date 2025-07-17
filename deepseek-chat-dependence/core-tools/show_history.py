import argparse
import os
import json

def show_history():
    history_dir = os.getenv('HISTORY_DIR')
    # 检查历史记录目录是否存在
    if not os.path.exists(history_dir):
        print(f"历史记录目录不存在: {history_dir}")
        return
    
    # 获取会话名称的环境变量
    session = os.getenv('SESSION')
    
    # 构建历史记录文件路径
    history_file = os.path.join(history_dir, f"{session}.json")
    
    # 检查历史记录文件是否存在
    if not os.path.isfile(history_file):
        print(f"未找到会话 {session} 的历史记录文件: {history_file}")
        return
    
    # 读取并打印历史记录
    print(f"会话 {session} 的历史记录:")
    with open(history_file, 'r', encoding='utf-8') as file:
        history_data = json.load(file)
        for entry in history_data:
            role = entry.get('role')
            answer = entry.get('content')
            print(f"来自: {role}\n")
            print(f"说: {answer}\n")

show_history()