import argparse
import os
import json

def clear_history():
    history_dir = os.getenv('HISTORY_DIR')
    if not history_dir or not os.path.exists(history_dir):
        print(f"历史记录目录不存在或未设置: {history_dir}")
        return
    
    # 获取会话名称的环境变量
    session = os.getenv('SESSION')
    
    # 构建历史记录文件路径
    history_file = os.path.join(history_dir, f"{session}.json")
    
    # 检查历史记录文件是否存在
    if not os.path.isfile(history_file):
        print(f"未找到会话 {session} 的历史记录文件: {history_file}")
    
    # 删除历史记录文件
    try:
        os.remove(history_file)
        print(f"已清除会话 {session} 的历史记录。")
    except Exception as e:
        print(f"删除历史记录文件时出错: {e}")

clear_history()