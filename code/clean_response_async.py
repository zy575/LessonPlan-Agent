import pandas as pd
import json
import os 
import re
import sys
import random
import concurrent.futures
from utils.utils import *
from utils.data_info import *
from utils.subject_path import *
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

def get_all_id(id_path):
    id_list = []
    with open(id_path, 'r') as f:
        id_temp = json.load(f)
    for _,id_item in id_temp.items():
        id_list += [item['id'] for item in id_item]
    return id_list
def get_data_from_dir(test_dir):
    data = []
    id_list = get_all_id('../data/sample_ids_0117_eval.json')
    for file_path in Path(test_dir).rglob("*.json"):
        if '_example_0_tb_type_0' not in file_path.stem:continue
        with open(file_path, "r") as f:
            temp = json.load(f)
        data += [{**item, 'file_name': file_path.stem} for item in temp if item['id'] in id_list]
    return data

def get_process_from_dir(process_dir):
    data = []
    id_list = get_all_id('../data/sample_ids_0117_eval.json')
    rtb = get_tb("../result/rewrite_tb/2025-01-17",'tips')
    for file_path in Path(process_dir).rglob("*.json"):
        if '教学过程' in file_path.stem:
            if 'example_0_tb_type_1' in file_path.stem: continue
            if '科学' in file_path.stem: continue
            with open(file_path, "r") as f:
                item = json.load(f)
                if item['id'] not in id_list:
                    print("id not in id_list", item['id'])
                    continue
                h1_contents = extract_h1_with_subcontent(item['response'])
                try:
                    tb_contents = extract_h1_with_subcontent(rtb[item['id']])
                except:
                    # print(item['id'])
                    continue
                if len(h1_contents) != len(tb_contents):
                    print("长度不相等：",item['id'])
                    continue
                cnt = 0
                pattern = r"<h1>.*?</h1>"
                for i in range(len(h1_contents)):
                    tb_temp = re.sub(pattern, "", tb_contents[i])
                    data.append({'id':item['id'],'subject':item['subject'],'lesson_info':item['lesson_info'],'stage_time':item['teach_stage'],'rank':cnt,'stage':h1_contents[i], 'textbook':tb_temp, 'save_dir':item['save_dir']})
                    cnt += 1
    return data

def get_process_from_dir_tb(process_dir):
    data = []
    id_list = get_all_id('../data/sample_ids_0117_eval.json')
    rtb = get_tb("../result/rewrite_tb/2025-01-17",'tips')
    for file_path in Path(process_dir).rglob("*.json"):
        if '教学过程' in file_path.stem:
            if 'example_0_tb_type_1' in file_path.stem: continue
            # if '数学' not in file_path.stem: continue
            with open(file_path, "r") as f:
                item = json.load(f)
                if item['id'] not in id_list:continue
                h1_contents = extract_h1_with_subcontent(item['response'])
                try:
                    tb_contents = extract_h1_with_subcontent(rtb[item['id']])
                except:
                    # print(item['id'])
                    continue
                if len(h1_contents) != len(tb_contents):
                    print("长度不相等：",1111)
                    print("长度不相等：",item['id'])
                    cnt = 0
                    pattern = r'<h1>(.*?)</h1>'
                    matches = re.findall(pattern, rtb[item['id']])

                    # 将匹配结果转换为字典
                    # result_dict = {key.strip(): value.strip() for key, value in matches}

                    print("长度不相等：",matches)
                    # for i in range(len(h1_contents)):
                    #     for key, value in result_dict.items():
                    #         if key in h1_contents[i]:
                    #             data.append({'id':item['id'],'subject':item['subject'],'lesson_info':item['lesson_info'],'stage_time':item['teach_stage'],'rank':cnt,'stage':h1_contents[i], 'textbook':value, 'save_dir':item['save_dir']})
                    #             cnt += 1
                else:
                    cnt = 0
                    pattern = r"<h1>.*?</h1>"
                    for i in range(len(h1_contents)):
                        tb_temp = re.sub(pattern, "", tb_contents[i])
                        data.append({'id':item['id'],'subject':item['subject'],'lesson_info':item['lesson_info'],'stage_time':item['teach_stage'],'rank':cnt,'stage':h1_contents[i], 'textbook':tb_temp, 'save_dir':item['save_dir']})
                        cnt += 1
    return data
        
def get_sta_from_dir(root_dir):
    data = []
    id_list = get_all_id('../data/sample_ids_1224_eval.json')
    # rtb = get_tb("../result/rewrite_tb/2024-12-24/core")
    for file_path in Path(root_dir).rglob("*.json"):
        if '学情分析' in file_path.stem:
            with open(file_path, "r") as f:
                item = json.load(f)
            if 'example_0_tb_type_1' in item['save_dir']: continue
            if item['id'] not in id_list:continue
            pre_kp_path = os.path.join(subject_kp_path[item['subject']],get_previous_id(item['id'])+'.json')
            now_kp_path = os.path.join(subject_kp_path[item['subject']], item['id']+'.json')
            if os.path.exists(pre_kp_path):
                with open(pre_kp_path, "r") as f:
                    pre_kp_data = json.load(f)
                    pre_kp = pre_kp_data['tips']
            else:
                pre_kp = ''
            if os.path.exists(now_kp_path):
                with open(now_kp_path, "r") as f:
                    now_kp_data = json.load(f)
                    now_kp = now_kp_data['tips']
            else:
                now_kp = ''
            item['pre_response'] = item['response']
            item['pre_kp'] = pre_kp
            item['now_kp'] = now_kp
            data.append(item)
            
    return data


        
def get_eval_from_dir(root_dir, process_dir):
    data = []
    id_list = get_all_id('../data/sample_ids_1224_eval.json')
    # rtb = get_tb("../result/rewrite_tb/2024-12-24/core")
    process_temp = []
    for file_path in Path(process_dir).rglob("*.json"):
        with open(file_path, "r") as f:
            process_temp += json.load(f)
    process = {item['id']:item['response'] for item in process_temp if item['module'] == '教学过程'}
    for file_path in Path(root_dir).rglob("*.json"):
        if '教学评价' in file_path.stem:
            with open(file_path, "r") as f:
                item = json.load(f)
            if 'example_0_tb_type_1' in item['save_dir']: continue
            if item['id'] not in id_list:continue
            item['process'] = process[item['id']]
            item['pre_response'] = item['response']
            if item['subject'] == '化学':
                item['example'] = '''
                在课堂评估中需要体现纪律管理和时间管理：
                <h1>学生评估</h1>1. 理解元素周期律的基本概念：通过提问学生元素周期律的定义和基本概念，评估他们的理解。课后通过作业和测验来检查学生对核心概念的掌握。
                2. 数据分析能力：通过分析表5-1和表5-2中的数据，评估学生的逻辑思维能力和数据分析能力。可以让学生绘制图表并解释数据变化规律。
                3. 实验操作能力：通过观察学生进行钠、镁、铝金属性实验的操作，评估他们的实验设计和数据处理能力。可以让学生记录实验现象并总结实验结论。
                <h1>教师评估</h1>通过反思“课程导入”和“总结评价”环节，评估教学设计是否符合学生的认知水平。在“总结评价”环节，观察学生是否能够正确总结本堂课的知识点，如元素周期律的基本概念、原子半径和化合价的变化规律，根据学生的总结情况来判断教学方法是否有效。
                <h1>课堂评估</h1>1. 课堂纪律：在“小组协作，解决问题”环节，观察学生的行为表现，评估课堂纪律情况，比如学生是否能认真进行实验和讨论，是否出现课堂混乱和打闹的情况。教师可以在学生讨论前明确讨论内容和实践，并在活动中进行适时提醒。
                2. 时间管理：评估各教学环节的时间安排是否合理，在“围绕主题，明确问题”环节，确保学生有足够的时间进行数据分析和讨论。在“总结评价”环节，确保有足够的时间进行课堂小结和布置作业。教师可以在课后反思每个环节的时间安排，记录哪些环节时间过长或过短，并在下次教学中进行调整。
                '''
            else:
                item['example'] = '''
                ```
                教学过程有个活动是写圣诞卡片，因此下面的教学评价结合了写圣诞卡片的活动：
                <h1>学生评估</h1>
                观察学生在课堂上的表现,如是否积极参与写圣诞卡片的活动,是否能够正确使用圣诞节相关的词汇和句型来评估学生的学习态度和学习效果。通过检查学生完成的圣诞卡片,评估他们的书写能力和创意表达。
                <h1>教师评估</h1>
                首先,通过观察学生在写圣诞卡片活动中的表现,评估教学效果。其次,通过学生的反馈和表现,评估教学内容和方法是否适合学生,是否能够激发学生的学习兴趣。最后,通过与同事的交流和讨论,获取更多的教学建议和反馈,以便不断提高教学水平。
                <h1>课堂评估</h1>
                首先,通过观察课堂氛围,如学生在写圣诞卡片活动中的参与度,课堂的互动性等,评估课堂的教学效果。其次,通过学生家长对于圣诞卡片活动的反馈,评估课堂的教学内容和方法是否有效。最后,通过对课堂的录像或记录进行分析,了解课堂的教学过程,以便对教学进行改进和优化。
```
                '''
            data.append(item)
            
    return data

def generate_StepByStep_one(data_item,save_dir,get_type, model=' ', temperature=0.01, use_example=True):
# def generate_StepByStep(data_item,save_dir,get_type, model='gpt-4o', temperature=0.01, use_example=True):
    tb_content = get_tb("../result/kp_content/2024-12-30/core",'tips')
    if get_type == 'step_one':
        task_prompt_system = load_prompt("clean_response_step_one")
        task_prompt_template = load_prompt("clean_response_step_one_template")
        task_prompt_template = task_prompt_template.format(
            data_item['subject'],
            data_item['lesson_info'],
            data_item['module'],
            '',
            data_item['response'],
        )
    print("task_prompt_template",task_prompt_template)
    question = f"<Action> generate_module </Action>\n<system start>\n{task_prompt_system}<system end>\n<input start>\n{task_prompt_template}<input end>"
    print("=======",question)
    if model == 'gpt-4o':
        reply = send_chat_request(
        '', examples=[], question=question, temperature=temperature, engine=model, priority=10,max_tokens=4096
        )
    else:
        reply = send_chat_request_async(
            '', examples=[], question=question, temperature=temperature, engine=model, priority=10,max_tokens=4096
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
    tb_content = get_tb("../result/kp_content/2024-12-10/core",'tips')
    task_prompt_system = load_prompt("check_stage_system")
    task_prompt_template = load_prompt("check_stage_template")
    task_prompt_template = task_prompt_template.format(
        data_item['subject'],
        data_item['lesson_info'],
        data_item['textbook'],
        data_item['stage'],
    )
    print("task_prompt_template",task_prompt_template)
    question = f"<Action> generate_module </Action>\n<system start>\n{task_prompt_system}<system end>\n<input start>\n{task_prompt_template}<input end>"
    print("=======",question)
    if model == 'gpt-4o':
        reply = send_chat_request(
        '', examples=[], question=question, temperature=temperature, engine=model, priority=10,max_tokens=4096
        )
    else:
        reply = send_chat_request_async(
            '', examples=[], question=question, temperature=temperature, engine=model, priority=10,max_tokens=4096
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


def generate_StepByStep_two(data_item, model=' ', temperature=0.01, use_example=True):
# def generate_StepByStep(data_item,save_dir,get_type, model='gpt-4o', temperature=0.01, use_example=True):
    tb_content = get_tb("../result/kp_content/2024-12-10/core",'tips')
    task_prompt_system = load_prompt("check_stage_system")
    task_prompt_template = load_prompt("check_stage_template")
    task_prompt_template = task_prompt_template.format(
        data_item['subject'],
        data_item['lesson_info'],
        data_item['textbook'],
        data_item['stage'],
    )
    print("task_prompt_template",task_prompt_template)
    question = f"<Action> generate_module </Action>\n<system start>\n{task_prompt_system}<system end>\n<input start>\n{task_prompt_template}<input end>"
    print("=======",question)
    if model == 'gpt-4o':
        reply = send_chat_request(
        '', examples=[], question=question, temperature=temperature, engine=model, priority=10,max_tokens=4096
        )
    else:
        reply = send_chat_request_async(
            '', examples=[], question=question, temperature=temperature, engine=model, priority=10,max_tokens=4096
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

def generate_StepByStep_sta(data_item, model=' ', temperature=0.01, use_example=True):
# def generate_StepByStep(data_item,save_dir,get_type, model='gpt-4o', temperature=0.01, use_example=True):
    tb_content = get_tb("../result/kp_content/2024-12-10/core",'tips')
    task_prompt_system = load_prompt("check_sta_system")
    task_prompt_template = load_prompt("check_sta_template")
    task_prompt_template = task_prompt_template.format(
        data_item['subject'],
        data_item['lesson_info'],
        data_item['pre_kp'],
        data_item['textbook'],
        data_item['pre_response'],
    )
    print("task_prompt_template",task_prompt_template)
    question = f"<Action> generate_module </Action>\n<system start>\n{task_prompt_system}<system end>\n<input start>\n{task_prompt_template}<input end>"
    print("=======",question)
    if model == 'gpt-4o':
        reply = send_chat_request(
        '', examples=[], question=question, temperature=temperature, engine=model, priority=10,max_tokens=4096
        )
    else:
        reply = send_chat_request_async(
            '', examples=[], question=question, temperature=temperature, engine=model, priority=10,max_tokens=4096
        )
    # reply = send_chat_request(
    #     '', examples=[], question=question, temperature=temperature, engine=model, priority=10
    # )
    # Ensure the directory exists
    save_dir = os.path.join(data_item['save_dir'],'sta')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, data_item['id'] + '.json')
    data_item['response'] = reply['response']
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(data_item, f, ensure_ascii=False, indent=4)
    print(f"File saved successfully at {save_path}")


def generate_StepByStep_eval(data_item, model=' ', temperature=0.01, use_example=True):
# def generate_StepByStep(data_item,save_dir,get_type, model='gpt-4o', temperature=0.01, use_example=True):
    tb_content = get_tb("../result/kp_content/2024-12-10/core",'tips')
    task_prompt_system = load_prompt("check_eval_system") +'\n'+ data_item['example']
    task_prompt_template = load_prompt("check_eval_template")
    task_prompt_template = task_prompt_template.format(
        data_item['subject'],
        data_item['process'],
        data_item['pre_response'],
    )
    print("task_prompt_template",task_prompt_template)
    question = f"<Action> generate_module </Action>\n<system start>\n{task_prompt_system}<system end>\n<input start>\n{task_prompt_template}<input end>"
    print("=======",question)
    if model == 'gpt-4o':
        reply = send_chat_request(
        '', examples=[], question=question, temperature=temperature, engine=model, priority=10,max_tokens=4096
        )
    else:
        reply = send_chat_request_async(
            '', examples=[], question=question, temperature=temperature, engine=model, priority=10,max_tokens=4096
        )
    # reply = send_chat_request(
    #     '', examples=[], question=question, temperature=temperature, engine=model, priority=10
    # )
    # Ensure the directory exists
    save_dir = os.path.join(data_item['save_dir'],'eval')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, data_item['id'] + '.json')
    data_item['response'] = reply['response']
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(data_item, f, ensure_ascii=False, indent=4)
    print(f"File saved successfully at {save_path}")

def get_clean_data_step_one(is_async,root_dir):
    
    save_dir = "../result/clean_data"
    save_dir = get_save_dir(save_dir)
    topics = get_data_from_dir(root_dir)
    print(len(topics))
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
            
def get_clean_data_step_two(is_async, root_dir):
    # root_dir = "../result/clean_data/2024-12-24"
    topics = get_process_from_dir(root_dir)
    print(len(topics))
    print(topics[0])
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



def get_clean_data_sta(is_async, root_dir):
    topics = get_sta_from_dir(root_dir)
    n_jobs = 300
    print(len(topics))
    n_jobs = min(n_jobs, len(topics))
    get_type = 'step_one'
    set_log(root_dir)
    if is_async:
        with concurrent.futures.ThreadPoolExecutor(max_workers=n_jobs) as executor:
            futures = [executor.submit(generate_StepByStep_sta, topic) for topic in topics]
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
                generate_StepByStep_sta(topic, model='gpt-4o')
            except Exception as e:
                print("An error occurred:")
                print(f"Type: {type(e).__name__}")
                print(f"Message: {e}")
                # 打印详细的堆栈跟踪，包括文件名、行号和函数名称
                tb_str = ''.join(traceback.format_tb(e.__traceback__))
                print("Traceback details:")
                print(tb_str)

def get_clean_data_eval(is_async, root_dir, process_path):
    topics = get_eval_from_dir(root_dir, process_path)
    n_jobs = 300
    print(len(topics))
    n_jobs = min(n_jobs, len(topics))
    get_type = 'step_one'
    set_log(root_dir)
    if is_async:
        with concurrent.futures.ThreadPoolExecutor(max_workers=n_jobs) as executor:
            futures = [executor.submit(generate_StepByStep_eval, topic) for topic in topics]
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
                generate_StepByStep_eval(topic, model='gpt-4o')
            except Exception as e:
                print("An error occurred:")
                print(f"Type: {type(e).__name__}")
                print(f"Message: {e}")
                # 打印详细的堆栈跟踪，包括文件名、行号和函数名称
                tb_str = ''.join(traceback.format_tb(e.__traceback__))
                print("Traceback details:")
                print(tb_str)

is_async = False
# one_root_dir = "../result/evel_data/2025-01-17"
two_root_dir = "../result/clean_data/2025-01-19"
# sta_root_dir = "../result/clean_data/2024-12-29/step_one/test_data_英语_example_0_tb_type_0"
# eval_root_dir = "../result/clean_data/2025-01-15"
# process_dir = "../result/unit_eval_data/2024-12-30"
# get_clean_data_step_one(is_async,one_root_dir)
# get_clean_data_sta(is_async, sta_root_dir)
# get_clean_data_eval(is_async, eval_root_dir, process_dir)
get_clean_data_step_two(is_async,two_root_dir)