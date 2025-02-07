import pandas as pd
import json
import os 
import re
import sys
import random
import concurrent.futures
from utils.utils import *
from utils.data_info import *
from pathlib import Path
import traceback
from pathlib import Path
old_stdout = sys.stdout
old_stderr = sys.stderr
from call_gpt.call_gpt import (
    send_chat_request,
    send_chat_request_async,
    run_multi_send_chat_request,
)

def get_data_from_dir(test_dir):
    data = []
    for file_path in Path(test_dir).rglob("*.json"):
        with open(file_path, "r") as f:
            temp = json.load(f)
        temp = temp[:50]
        data += [{**item, 'file_name': file_path.stem} for item in temp]
    return data

def get_data_from_dir_temp(test_dir):
    data = []
    for file_path in Path(test_dir).rglob("*.json"):
        if 'example_0_tb_type_0' in file_path.stem:
            with open(file_path, "r") as f:
                temp = json.load(f)
            temp = temp[:50]
            data += [{**item, 'file_name': file_path.stem} for item in temp]
    return data


# def generate_StepByStep(data_item,save_dir,get_type, model=' ', temperature=0.01, use_example=True):
def generate_StepByStep(data_item,save_dir,get_type, model='gpt-4o', temperature=0.01, use_example=True):
    if get_type == 'step_one':
        task_prompt_system = load_prompt("clean_response_step_one")
        task_prompt_template = load_prompt("clean_response_step_one_template")
        task_prompt_template = task_prompt_template.format(
            data_item['subject'],
            data_item['lesson_info'],
            data_item['module'],
            data_item['textbook'],
            data_item['response'],
        )
    print("task_prompt_template",task_prompt_template)
    question = f"<Action> generate_module </Action>\n<system start>\n{task_prompt_system}<system end>\n<input start>\n{task_prompt_template}<input end>"
    print("=======",question)
    reply = send_chat_request(
        '', examples=[], question=question, temperature=temperature, engine=model, priority=10
    )
    # reply = send_chat_request(
    #     '', examples=[], question=question, temperature=temperature, engine=model, priority=10
    # )
    # Ensure the directory exists
    save_dir = os.path.join(save_dir, get_type,data_item['file_name'])
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, data_item['id']+'_'+data_item['module']+'.json')
    data_item['tips'] = reply['response']
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(data_item, f, ensure_ascii=False, indent=4)
    print(f"File saved successfully at {save_path}")




root_dir = "../result/evel_data/2024-12-10"
save_dir = "../result/clean_data_temp"
save_dir = get_save_dir(save_dir)
test_data = ""
clean_type = ""
topics = get_data_from_dir_temp(root_dir)
n_jobs = 300
n_jobs = min(n_jobs, len(topics))
get_type = 'step_one'
set_log(save_dir)
for item in topics:
    try:
        generate_StepByStep(item, save_dir,get_type)
    except Exception as e:
        print("An error occurred:")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {e}")
        # 打印详细的堆栈跟踪，包括文件名、行号和函数名称
        tb_str = ''.join(traceback.format_tb(e.__traceback__))
        print("Traceback details:")
        print(tb_str)
# with concurrent.futures.ThreadPoolExecutor(max_workers=n_jobs) as executor:
#     futures = [executor.submit(generate_StepByStep, topic,save_dir, get_type) for topic in topics]
#     for future in concurrent.futures.as_completed(futures):
#         try:
#             future.result()
#         except Exception as e:
#             print("An error occurred:")
#             print(f"Type: {type(e).__name__}")
#             print(f"Message: {e}")
#             # 打印详细的堆栈跟踪，包括文件名、行号和函数名称
#             tb_str = ''.join(traceback.format_tb(e.__traceback__))
#             print("Traceback details:")
#             print(tb_str)