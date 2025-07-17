import json
import os
from openai import OpenAI
from datetime import datetime

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

def replace_file_references(messages):
    """替换消息中的文件引用为实际内容"""
    processed_messages = []
    
    for message in messages:
        if message["role"] == "file":
            try:
                # 获取绝对路径
                current_dir = os.getcwd()
                abs_path = os.path.join(current_dir, message["content"])
                
                # 读取文件内容
                with open(abs_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # 添加文件头信息
                file_info = f"文件内容: {message['content']}\n\n{content}"
                
                # 替换为实际内容
                processed_messages.append({
                    "role": "user",
                    "content": file_info
                })
                
                print(f"已加载文件: {message['content']}")
                
            except FileNotFoundError:
                error_msg = f"错误: 文件未找到 - {message['content']}"
                processed_messages.append({
                    "role": "user",
                    "content": error_msg
                })
                print(error_msg)
                
            except Exception as e:
                error_msg = f"读取文件出错: {message['content']} - {str(e)}"
                processed_messages.append({
                    "role": "user",
                    "content": error_msg
                })
                print(error_msg)
        else:
            processed_messages.append(message)
    
    return processed_messages

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
    
    get_data=[]
    # 1. 读取现有JSON文件
    with open(json_file_path, 'r', encoding='utf-8') as rf:
        get_data = json.load(rf)  # 这会得到一个Python列表
    # 2. 判断是否增加了提示词
    if get_data[0].get("role") != "system":
        get_data.insert(0, sysmes[0])  # 在列表开头添加系统消息
    # 3. 添加新字典到列表中
    get_data.append(record)

    # 4. 写回文件
    with open(json_file_path, 'w', encoding='utf-8') as wf:
        json.dump(get_data, wf, ensure_ascii=False, indent=4)  # indent参数使输出更易读




def get_streaming_response(messages):
    full_response = ""
    #获取流式响应
    #:param messages: 消息列表
    #:return: 完整的回复内容
    
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        raise ValueError("未设置环境变量 DEEPSEEK_API_KEY")
    
    model_url=os.getenv('MODEL_URL')
    if not model_url:
        model_url = "https://api.deepseek.com"
    
    model_name= os.getenv('MODEL_NAME')
    if not model_name:
        model_name = "deepseek-reasoner"
    client = OpenAI(
        api_key=api_key,
        base_url=model_url
    )
    
    stream = client.chat.completions.create(
        model=model_name,
        messages=messages,
        stream=True
    )
    
    
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content is not None:
            print(content, end='', flush=True)
            #os.system("say '"+content+"'")  # 使用系统语音朗读内容
            full_response += content
    
    print()  # 确保有换行
    return full_response


message= os.getenv('QUESTION')
if not message:
    raise ValueError("未设置环境变量 QUESTION")

save_history("user",message)


history_dir = os.getenv('HISTORY_DIR')
# 检查历史记录目录是否存在
if not history_dir or not os.path.exists(history_dir):
    print(f"历史记录目录不存在: {history_dir}")

# 获取会话名称的环境变量
session = os.getenv('SESSION')

# Ensure history_dir and session are not None before joining paths
if not history_dir or not session:
    raise ValueError("HISTORY_DIR 或 SESSION 环境变量未设置")
history_file = os.path.join(history_dir, f"{session}.json")
max_history = 2*int(os.getenv('MAX_HISTORY', 100))  # 默认使用的最大历史记录数为100

# 读取历史记录
with open(history_file, 'r', encoding='utf-8') as file:
    history_data = json.load(file)
history_data = replace_file_references(history_data)  # 替换文件引用为实际内容
# 获取最后 max_history 组数据
last_history = history_data[-max_history:] if len(history_data) >= max_history else history_data

full_response=get_streaming_response(last_history)

save_history("assistant", full_response)
