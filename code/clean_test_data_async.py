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
def extract_h1_with_subcontent(html):
    # 使用非贪婪模式匹配 <h1> 开头到下一个 <h1> 或文档结尾之间的内容
    pattern = re.compile(r'(<h1>.*?</h1>(?:(?!<h1>).)*)', re.DOTALL)
    matches = pattern.findall(html)
    return matches
def get_data_from_dir(test_dir):
    data = []
    for file_path in Path(test_dir).rglob("*.json"):
        # if 'test_data_化学_example_0_tb_type_0' in file_path.stem:
        with open(file_path, "r") as f:
            temp = json.load(f)
        # temp = temp[:140]
        data += [{**item, 'file_name': file_path.stem} for item in temp]
    return data

def get_process_from_dir(process_dir):
    data = []
    for file_path in Path(process_dir).rglob("*.json"):
        if '教学过程' in file_path.stem:
            with open(file_path, "r") as f:
                item = json.load(f)
                if 'example_0_tb_type_0' not in item['save_dir']:continue
                h1_contents = extract_h1_with_subcontent(item['tips'])
                cnt = 0
                for content in h1_contents:
                    data.append({'id':item['id'],'subject':item['subject'],'lesson_info':item['lesson_info'],'stage_time':item['teach_stage'],'rank':cnt,'stage':content, 'textbook':item['textbook'], 'save_dir':item['save_dir']})
                    cnt += 1
    return data
        

def generate_StepByStep_one(data_item,save_dir,get_type, model=' ', temperature=0.01, use_example=True):
# def generate_StepByStep(data_item,save_dir,get_type, model='gpt-4o', temperature=0.01, use_example=True):
    tb_content = get_tb("../result/kp_content/2024-12-10/core")
    if get_type == 'step_one':
        task_prompt_system = load_prompt("clean_response_step_one")
        task_prompt_template = load_prompt("clean_response_step_one_template")
        task_prompt_template = task_prompt_template.format(
            data_item['subject'],
            data_item['lesson_info'],
            data_item['module'],
            tb_content[data_item['id']],
            data_item['response'],
        )
    print("task_prompt_template",task_prompt_template)
    question = f"<Action> generate_module </Action>\n<system start>\n{task_prompt_system}<system end>\n<input start>\n{task_prompt_template}<input end>"
    print("=======",question)
    if model == 'gpt-4o':
        reply = send_chat_request(
        '', examples=[], question=question, temperature=temperature, engine=model, priority=10
        )
    else:
        reply = send_chat_request_async(
            '', examples=[], question=question, temperature=temperature, engine=model, priority=10
        )
    # reply = send_chat_request(
    #     '', examples=[], question=question, temperature=temperature, engine=model, priority=10
    # )
    # Ensure the directory exists
    save_dir = os.path.join(save_dir, get_type,data_item['file_name'])
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    data_item['save_dir'] = save_dir
    save_path = os.path.join(save_dir, data_item['id']+'_'+data_item['module']+'.json')
    data_item['tips'] = reply['response']
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(data_item, f, ensure_ascii=False, indent=4)
    print(f"File saved successfully at {save_path}")

def generate_StepByStep_two(data_item, model=' ', temperature=0.01, use_example=True):
# def generate_StepByStep(data_item,save_dir,get_type, model='gpt-4o', temperature=0.01, use_example=True):
    tb_content = get_tb("../result/kp_content/2024-12-10/core")
    task_prompt_system = load_prompt("clean_response_step_two")
    task_prompt_template = load_prompt("clean_response_step_two_template")
    task_prompt_template = task_prompt_template.format(
        data_item['subject'],
        data_item['lesson_info'],
        tb_content[data_item['id']],
        data_item['stage'],
    )
    print("task_prompt_template",task_prompt_template)
    question = f"<Action> generate_module </Action>\n<system start>\n{task_prompt_system}<system end>\n<input start>\n{task_prompt_template}<input end>"
    print("=======",question)
    if model == 'gpt-4o':
        reply = send_chat_request(
        '', examples=[], question=question, temperature=temperature, engine=model, priority=10
        )
    else:
        reply = send_chat_request_async(
            '', examples=[], question=question, temperature=temperature, engine=model, priority=10
        )
    # reply = send_chat_request(
    #     '', examples=[], question=question, temperature=temperature, engine=model, priority=10
    # )
    # Ensure the directory exists
    save_dir = os.path.join(data_item['save_dir'],'process')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, data_item['id'] + '_' + str(data_item['rank']) + '.json')
    data_item['stage_response'] = reply['response']
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(data_item, f, ensure_ascii=False, indent=4)
    print(f"File saved successfully at {save_path}")

def get_clean_data_step_one(is_async = True):
    root_dir = "../result/evel_data/2024-12-10"
    save_dir = "../result/clean_data"
    save_dir = get_save_dir(save_dir)
    topics = get_data_from_dir(root_dir)
    n_jobs = 300
    n_jobs = min(n_jobs, len(topics))
    get_type = 'step_one'
    set_log(save_dir)
    if is_async:
        with concurrent.futures.ThreadPoolExecutor(max_workers=n_jobs) as executor:
            futures = [executor.submit(generate_StepByStep_one, topic,save_dir, get_type) for topic in topics]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print("An error occurred:")
                    print(f"Type: {type(e).__name__}")
                    print(f"Message: {e}")
                    # 打印详细的堆栈跟踪，包括文件名、行号和函数名称
                    tb_str = ''.join(traceback.format_tb(e.__traceback__))
                    print("Traceback details:")
                    print(tb_str)
    else:
        for topic in topics:
            try:
                generate_StepByStep_one(topic, save_dir, get_type, model='gpt-4o')
            except Exception as e:
                print("An error occurred:")
                print(f"Type: {type(e).__name__}")
                print(f"Message: {e}")
                # 打印详细的堆栈跟踪，包括文件名、行号和函数名称
                tb_str = ''.join(traceback.format_tb(e.__traceback__))
                print("Traceback details:")
                print(tb_str)
            
def get_clean_data_step_two(is_async=True):
    root_dir = "../result/clean_data/2024-12-11"
    topics = get_process_from_dir(root_dir)
    n_jobs = 300
    n_jobs = min(n_jobs, len(topics))
    get_type = 'step_one'
    set_log(root_dir)
    if is_async:
        with concurrent.futures.ThreadPoolExecutor(max_workers=n_jobs) as executor:
            futures = [executor.submit(generate_StepByStep_two, topic) for topic in topics]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print("An error occurred:")
                    print(f"Type: {type(e).__name__}")
                    print(f"Message: {e}")
                    # 打印详细的堆栈跟踪，包括文件名、行号和函数名称
                    tb_str = ''.join(traceback.format_tb(e.__traceback__))
                    print("Traceback details:")
                    print(tb_str)
    else:
        for topic in topics:
            try:
                generate_StepByStep_two(topic, model='gpt-4o')
            except Exception as e:
                print("An error occurred:")
                print(f"Type: {type(e).__name__}")
                print(f"Message: {e}")
                # 打印详细的堆栈跟踪，包括文件名、行号和函数名称
                tb_str = ''.join(traceback.format_tb(e.__traceback__))
                print("Traceback details:")
                print(tb_str)

is_async = False
get_clean_data_step_one(is_async)
get_clean_data_step_two(is_async)