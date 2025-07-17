import os
import sys
import re
import json




def remove_files():
    # data含有：role,assistant
    # 获取环境变量
    history_dir = os.getenv('HISTORY_DIR')
    session_name = os.getenv('SESSION')
    
    if history_dir is None:
        raise ValueError("环境变量 HISTORY_DIR 未设置")
    if session_name is None:
        raise ValueError("环境变量 SESSION 未设置")
    
    # 定义 JSON 文件路径
    json_file_path = os.path.join(history_dir, session_name + '.json')

    prompt = os.getenv('SET_PROMPT')
    if prompt == "":
        prompt = "你是一个智能助手，旨在回答用户的问题。请根据用户的提问提供准确和有用的答案。"
    sysmes = [{
        "role": "system",
        "content": prompt
    }]
    
    get_data=[]
    # 1. 读取现有JSON文件
    with open(json_file_path, 'r', encoding='utf-8') as rf:
        get_data = json.load(rf)  # 这会得到一个Python列表
    # 2. 删除引用文件
    i = 0
    while i < len(get_data):
        if get_data[i].get("role") == "file":
            get_data.remove(get_data[i])
        i += 1
    # 4. 写回文件
    with open(json_file_path, 'w', encoding='utf-8') as wf:
        json.dump(get_data, wf, ensure_ascii=False, indent=4)  # indent参数使输出更易读




def remove_file_reference():
    remove_files()
    print("文件引用已清空")



def main():
    
    # 清空文件引用
    remove_file_reference()

main()


