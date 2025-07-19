import os
import sys
import re
import json



def get_relative_file_path(file_path):
    """获取文件相对于当前工作目录的路径"""
    
    # 获取文件的绝对路径
    abs_path = os.path.abspath(file_path)
    
    # 确保文件存在
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"文件不存在: {abs_path}")
    
    # 获取相对路径
    relative_path = os.path.relpath(abs_path, os.getcwd())
    
    return relative_path

def is_json_file_empty(file_path):
    # 检查文件是否存在且大小是否为0
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return True
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            # 检查加载后的数据是否为空
            if not data:  # 适用于空字典{}、空列表[]等
                return True
    except json.JSONDecodeError:  # 文件内容不是有效JSON
        return True
    except Exception as e:
        print(f"Error reading file: {e}")
        return True
    
    return False


def save_history(rolerc, contentrc):
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
    if(is_json_file_empty(json_file_path)):
        # 如果文件为空或不存在，创建一个新的 JSON 数组
        with open(json_file_path, 'w') as json_file:
            json.dump(sysmes, json_file, ensure_ascii=False, indent=4)
    record = {
        "role": rolerc,
        "content": contentrc
    }
    print(record)
    get_data=[]
    # 1. 读取现有JSON文件
    with open(json_file_path, 'r', encoding='utf-8') as rf:
        get_data = json.load(rf)  # 这会得到一个Python列表
    # 2. 判断是否增加了提示词
    if get_data[0].get("role") != "system":
        get_data.insert(0, sysmes[0])  # 在列表开头添加系统消息
    # 3. 添加新字典到列表中
    get_data.append(record)
    # print(get_data)
    # 4. 写回文件
    with open(json_file_path, 'w', encoding='utf-8') as wf:
        json.dump(get_data, wf, ensure_ascii=False, indent=4)  # indent参数使输出更易读




def save_file_reference(file_path):
    """保存文件引用到历史记录"""
    relative_path = get_relative_file_path(file_path)
    save_history("file", relative_path)
    print("文件引用已保存到历史记录")



def main():
    # 获取环境变量 FILEPATH
    file_path = os.getenv('GET_FILEPATH')
    if not file_path:
        print("错误: 未设置环境变量 FILEPATH")
        sys.exit(1)
    
    # 保存文件引用到历史记录
    save_file_reference(file_path)

main()


