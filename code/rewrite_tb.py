# %%
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

old_stdout = sys.stdout
old_stderr = sys.stderr
from call_gpt.call_gpt import (
    send_chat_request,
    send_chat_request_async,
    run_multi_send_chat_request,
)
def get_all_id(id_path):
    id_list = []
    with open(id_path, 'r') as f:
        id_temp = json.load(f)
    for _,id_item in id_temp.items():
        id_list += [item['id'] for item in id_item]
    return id_list
def get_data_from_test(unit_dir, test_dir):
    id_list = get_all_id("../data/sample_ids_0117_eval.json")
    obj_contents, key_contents = get_ok(unit_dir)
    data = []
    for root, dirs, files in os.walk(test_dir):
        for file in files:
            if '科学' in file:
                continue
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                data_temp = json.load(f)
                data += [item for item in data_temp if item['id'] in id_list]
    topics = []
    ids_have = []
    for item in data:
        if item['id'] in ids_have:
            continue
        ids_have.append(item['id'])
        try:
            item['obj'] = obj_contents[item['id']]
        except:
            item['obj'] = ''
        try:
            item['key'] = key_contents[item['id']]
        except:
            item['key'] = ''
        topics.append(item)
    return topics
# %%
def get_extracted_str(data):
    rst = ''
    for item in data:
        rst += item.replace("提示内容：",'').replace("\n",'') +'\n'
    return rst

def load_prompt(
    prompt_name,
    prompt_path="./prompt/",
):
    task_prompt = open(f"{prompt_path}{prompt_name}.md", "r").read()
    return task_prompt



def generate_StepByStep(data_item,save_dir,get_type,is_async = True,is_ok = False, model=' ', temperature=0.01, use_example=True):
    pattern = r'\n\n提示内容：.*?\n(?=\n)'
    textbook_content = data_item['textbook']
    extracted_prompts = re.findall(pattern, textbook_content)
    # print("==========================")
    # print(tips_contents)
    textbook_content = re.sub(pattern, '', textbook_content)
    if is_ok:
        task_prompt_system = load_prompt("rewrite_tb_ok")+'\n'+rewrite_tb_ok_case[data_item['subject']]
        task_prompt_template = load_prompt("rewrite_tb_ok_template")
        task_prompt_template = task_prompt_template.format(
            data_item['subject'],
            data_item['level'],
            data_item['lesson_info'],
            data_item['teach_stage'],
            data_item['obj'],
            data_item['key'],
            textbook_content,
        )
    else:    
        task_prompt_system = load_prompt("rewrite_tb")+'\n'+rewrite_tb_case[data_item['subject']]
        task_prompt_template = load_prompt("rewrite_tb_template")
        task_prompt_template = task_prompt_template.format(
            data_item['subject'],
            data_item['level'],
            data_item['lesson_info'],
            data_item['teach_stage'],
            textbook_content,
        )
    print("task_prompt_template",task_prompt_template)
    question = f"<Action> generate_module </Action>\n<system start>\n{task_prompt_system}<system end>\n<input start>\n{task_prompt_template}<input end>"
    print("=======",question)
    if is_async:
        reply = send_chat_request_async(
            '', examples=[], question=question, temperature=temperature, engine=model, priority=10,max_tokens=4096
        )
    else:
        reply = send_chat_request(
            '', examples=[], question=question, temperature=temperature, engine='gpt-4o', priority=10,max_tokens=4096
        )
    # Ensure the directory exists
    save_dir = os.path.join(save_dir, get_type)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, data_item['id']+'.json')
    data_item['tips'] = reply['response']
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(data_item, f, ensure_ascii=False, indent=4)
    print(f"File saved successfully at {save_path}")


def rewrite_tb(date, is_async = True, is_ok = False):
    if is_ok:
        save_dir = "../result/rewrite_tb_ok"
    else:
        save_dir = "../result/rewrite_tb"
    unit_result = '../result/evel_data/'+date
    test_dir = '../result/evel_data/2025-01-17'
    log_path = '../log/' + save_dir.split('/')[-1]+'_output.log'
    log_file = open(log_path, "w", buffering=1)
    print('日志文件：', log_path)
    sys.stdout = log_file
    sys.stderr = log_file
    save_dir = get_save_dir(save_dir)
    topics = get_data_from_test(unit_result,test_dir)
    print(len(topics))
    print(topics[0])
    # topics = get_data_from_tb(root_dir)
    n_jobs = 300
    n_jobs = min(n_jobs, len(topics))
    get_type = 'core'
    if is_async:
        with concurrent.futures.ThreadPoolExecutor(max_workers=n_jobs) as executor:
            futures = [executor.submit(generate_StepByStep, topic,save_dir, get_type,is_async, is_ok) for topic in topics]
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
        for item in topics:
            try:
                generate_StepByStep(item, save_dir, get_type, is_async, is_ok)
            except Exception as e:
                print("An error occurred:")
                print(f"Type: {type(e).__name__}")
                print(f"Message: {e}")
                # 打印详细的堆栈跟踪，包括文件名、行号和函数名称
                tb_str = ''.join(traceback.format_tb(e.__traceback__))
                print("Traceback details:")
                print(tb_str)
if __name__ == '__main__':
    rewrite_tb('2025-01-17', False , False)