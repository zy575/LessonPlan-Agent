import os
from .data_info import *
import json
import copy
from datetime import datetime
import sys
import random
import re
import pandas as pd 
import glob
def get_id(df, data_info):
    temp = data_info.split("_")
    temp = temp[:-1]+temp[-1].split("@@@@")
    if len(temp) == 5:
        row = df[(df['学段'] == temp[0]) & (df['学科'] == temp[1]) & (df['教材'] == temp[2]) & (df['年级'] == temp[3]) & (df['一级目录'] == temp[4])]
    elif len(temp) == 6:
        row = df[(df['学段'] == temp[0]) & (df['学科'] == temp[1]) & (df['教材'] == temp[2]) & (df['年级'] == temp[3]) & (df['一级目录'] == temp[4]) & (df['二级目录'] == temp[5])]
    elif len(temp) == 7:
        row = df[(df['学段'] == temp[0]) & (df['学科'] == temp[1]) & (df['教材'] == temp[2]) & (df['年级'] == temp[3]) & (df['一级目录'] == temp[4]) & (df['二级目录'] == temp[5]) & (df['三级目录'] == temp[6])]
    elif len(temp) == 8:
        row = df[(df['学段'] == temp[0]) & (df['学科'] == temp[1]) & (df['教材'] == temp[2]) & (df['年级'] == temp[3]) & (df['一级目录'] == temp[4]) & (df['二级目录'] == temp[5]) & (df['四级目录'] == temp[7])]
    # 如果找到匹配的行，则返回第四列的值，否则返回None
    if not row.empty:
        return row.iloc[0]['id']
    else:
        return None
    
def get_textbook_topic(tb_value, parent_key=''):
    keys = []
    def recurse(current_data, current_path):
        for key, value in current_data.items():
            new_path = f"{current_path}@@@@{key}".strip('@@@@')
            if 'children' in value and value['children'] != {}:
                recurse(value['children'], new_path)
            else:
                # 如果没有更多的 children 字段，则将当前路径添加到列表中
                keys.append(new_path)

    if 'children' in tb_value:
        recurse(tb_value['children'], parent_key)
    
    return keys

def load_prompt(
    prompt_name,
    prompt_path="./prompt/",
):
    task_prompt = open(f"{prompt_path}{prompt_name}.md", "r").read()
    return task_prompt

def get_all_topics(root_dir):
    topics = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            # if file.split("_")[2] not in test_versions: continue
            file_path = os.path.join(root, file)
            info_temp = file.split('_')
            info_temp[-1] = info_temp[-1].split('.')[0]
            # if pre_version != '' and pre_version == info_temp[2]:
            #     file_cnt += 1
            # if pre_version == '' or pre_version != info_temp[2]:
            #     file_cnt = 0
            # if file_cnt > 5:
            #     continue
            pre_version = info_temp[2]
            with open(file_path, 'r') as f:
                data = json.load(f)
            print(file_path)
            all_topics = get_textbook_topic(data)
            print("all_topics",all_topics)
            # topics_temp = random.sample(all_topics, 5)
            lesson_info = '_'.join(info_temp)
            for topic_item in all_topics:
                id_temp = get_id(id_df, lesson_info+'_'+topic_item)
                if id_temp == None:continue
                topics.append({'id':id_temp, 'content':data, 'topic':topic_item,"lesson_info":lesson_info+'_'+topic_item,"info_temp":info_temp})
    return topics


def read_json(json_path):
    if ".jsonl" in json_path:
        json_data = []
        with open(json_path, "r") as file:
            for line in file:
                json_data.append(json.loads(line))
    else:
        with open(json_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
    return json_data


def get_textbook_topic(tb_value, parent_key=''):
    keys = []
    def recurse(current_data, current_path):
        for key, value in current_data.items():
            new_path = f"{current_path}@@@@{key}".strip('@@@@')
            if 'children' in value and value['children'] != {}:
                recurse(value['children'], new_path)
            else:
                # 如果没有更多的 children 字段，则将当前路径添加到列表中
                keys.append(new_path)

    if 'children' in tb_value:
        recurse(tb_value['children'], parent_key)
    
    return keys


def get_textbook_value(tb_topic, tb_value):
    if isinstance(tb_topic, list):
        topic_split = tb_topic
    if '@@@@' in tb_topic:
        topic_split = tb_topic.split("@@@@")
    else:
        topic_split = [tb_topic]
    # tb_value = tb_value["children"]
    for ts in topic_split:
        try:
            if "children" in tb_value and tb_value['children'] != {}:
                tb_value = tb_value["children"][ts]
            else:
                # print("\n-----",tb_value)
                tb_value = tb_value[ts]
        except Exception as e:
            return '暂无教材内容'
    return tb_value["content"]

def create_test_data(data, example_type, tb_type):
    item_list = []
    modules = ['教学内容分析','学情分析','教学目标','教学重难点','教学准备','教学过程','教学评价']
    for item in data:
    # if item['module'] != '学情分析':continue
        lesson_info = item['lesson_info']
        info_temp = lesson_info.split('_')
        kcs = info_temp[-1].split("@@@@")
        if tb_type == '1':
            tb_value = item['textbook']
        else:
            tb_value = '暂无教材内容'
        if len(kcs) > 2:
            chapter,theme = kcs[0], kcs[1]
            kc = ",".join(kcs[2:])
        elif len(kcs) == 2:
            chapter,theme = kcs[0], kcs[1]
            kc = ""
        else:
            chapter = kcs[0]
            theme,kc = "",""
        teach_mode = item['mode']
        for module in modules:
            if example_type == '0':
                example = ''
            elif  example_type == '1':
                try:
                    example = item['components_content'][module]
                except:
                    example = ''
            one_item = copy.deepcopy(item)
            one_item['module'] = module
            task_prompt_system = load_prompt("plan_generator_first_system")
            task_prompt_template = load_prompt("plan_generator_first_template")
            task_prompt_template = task_prompt_template.format(
                info_temp[1],
                module,
                info_temp[0],
                info_temp[2],
                info_temp[3],
                chapter,
                theme,
                kc,
                teach_mode,
                "",
                item['teach_stage'],
                tb_value,
                example,
            )
            question = f"<Action> generate_module </Action>\n<system start>\n{task_prompt_system}<system end>\n<input start>\n{task_prompt_template}<input end>"
            one_turn = [
                {"from": "human", "value": question},
                {"from": "gpt", "value": ''},
            ]
            one_item["conversations"] = one_turn
            # if one_item['module'] == '教学目标':  
            item_list.append(one_item)
    return item_list

def create_unit_test_data(data, example_type, tb_type):
    item_list = []
    modules = ['教学内容分析','学情分析','教学目标','教学重难点','教学准备','教学过程','教学评价']
    for item in data:
    # if item['module'] != '学情分析':continue
        lesson_info = item['lesson_info']
        info_temp = lesson_info.split('_')
        kcs = info_temp[-1].split("@@@@")
        if tb_type == '1':
            tb_value = item['textbook']
        else:
            tb_value = '暂无教材内容'
        if len(kcs) > 2:
            chapter,theme = kcs[0], kcs[1]
            kc = ",".join(kcs[2:])
        elif len(kcs) == 2:
            chapter,theme = kcs[0], kcs[1]
            kc = ""
        else:
            chapter = kcs[0]
            theme,kc = "",""
        teach_mode = item['mode']
        module = item['module']
        if example_type == '0':
            example = ''
        elif  example_type == '1':
            try:
                example = "这是一个示例，请不要照抄他"+item['response']
                # if module != '学情分析' and module != '教学过程' and module != '教学评价':
                #     example = ''
            except:
                example = ''
        one_item = copy.deepcopy(item)
        one_item['module'] = module
        # if module == '教学评价':
        #     tb_value = ''
        #     example = ''
        #     eval_str = item['tips']
        # else:
        #     eval_str = '' 
        task_prompt_system = load_prompt("plan_generator_first_system")
        task_prompt_template = load_prompt("plan_generator_first_template")
        task_prompt_template = task_prompt_template.format(
            info_temp[1],
            module,
            info_temp[0],
            info_temp[2],
            info_temp[3],
            chapter,
            theme,
            kc,
            teach_mode,
            "",
            item['teach_stage'],
            tb_value+example,
            ' ',
        )
        question = f"<Action> generate_module </Action>\n<system start>\n{task_prompt_system}<system end>\n<input start>\n{task_prompt_template}<input end>"
        one_turn = [
            {"from": "human", "value": question},
            {"from": "gpt", "value": ''},
        ]
        one_item["conversations"] = one_turn
        # if one_item['module'] == '教学目标':  
        item_list.append(one_item)
    return item_list

def get_save_dir(save_dir):
    current_datetime = datetime.now()
    current_data = current_datetime.strftime("%Y-%m-%d")
    save_dir = os.path.join(save_dir, current_data)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    return save_dir


def set_log(save_dir):
    log_path = '../log/' + save_dir.split('/')[-2]+'_'+save_dir.split('/')[-1]+'_output.log'
    log_file = open(log_path, "w", buffering=1)
    print('日志文件：', log_path)
    sys.stdout = log_file
    sys.stderr = log_file

def get_whole_process(process_dir):
    ids_contents = {}
    for root, dirs, files in os.walk(process_dir):
        
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                temp = json.load(f)
            id = file.split('_')[0]+'_'+file.split('_')[1]
            if id not in ids_contents:
                ids_contents[id] = ''
            if temp['rank'] == 0:
                ids_contents[id] = ''
            ids_contents[id] += temp['stage_response'].replace("```",'').replace("html",'') + '\n\n'
    return ids_contents

def get_whole_process_by_replace(process_dir):
    ids_contents = {}
    pattern = r'<h1>(.*?)<\/h1>'
    for root, dirs, files in os.walk(process_dir):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                temp = json.load(f)
            id = file.split('_')[0]+'_'+file.split('_')[1]
            if id not in ids_contents:
                ids_contents[id] = ''
            if temp['rank'] == 0:
                ids_contents[id] = ''
            stage_temp = temp['stage_response'].replace("```",'').replace("html",'')
            matches = re.findall(pattern, stage_temp, re.DOTALL)
            for match in matches:
                stage_temp_wo_title = stage_temp.replace(match, '')
                if len(stage_temp_wo_title) < 25:
                    stage_temp = '<h1> '+ match +' </h1>\n\n' + temp['textbook']
            ids_contents[id] += stage_temp + '\n\n'
    return ids_contents

def get_tb(tb_dir, key):
    ids_contents = {}
    for root, dirs, files in os.walk(tb_dir):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                temp = json.load(f)
            ids_contents[temp['id']] = temp[key]
    return ids_contents


def get_sta(tb_dir):
    ids_contents = {}
    for root, dirs, files in os.walk(tb_dir):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                temp = json.load(f)
            try:
                ids_contents[temp['id']] =  "<h1>前置知识点</h1>\n"+temp['pre_kp']+"\n<h1>本节知识点</h1>\n"+temp['now_kp']+"\n<h1>学生发展水平</h1>\n"
            except:
                ids_contents[temp['id']] =  ''
    return ids_contents

def get_data_by_unit(clean_data_dir, tb_data_dir):
    item_list = []
    process_dir = os.path.join(clean_data_dir, 'process')
    sta_dir = os.path.join(clean_data_dir, 'sta')
    eval_dir = os.path.join(clean_data_dir, 'eval')
    # sta_dir = sta_dir.replace('2024-12-29', '2024-12-24')
    process_contents = get_whole_process_by_replace(process_dir)
    sta_contents = get_sta(sta_dir)
    tb_contents = get_tb(tb_data_dir,'tips')
    eval_contents = get_tb(eval_dir,'response')
    # sta_contents = get_tb(sta_dir,'response')
    with open("../data/sample_ids_0117_eval.json", "r") as file:
        subject_ids = json.load(file) 
    id_list = []
    for subject, value in subject_ids.items():
        id_list += [item['id'] for item in value]
    for root, dirs, files in os.walk(clean_data_dir):
        if 'example_0_tb_type_1' in root: continue
        for file in files:
            module_type= file.split('_')[-1].split('.')[0]
            if 'example_0_tb_type_1' in root: continue
            if module_type in modules:
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if data['id'] not in id_list:
                    continue
                try:
                    data['textbook'] = tb_contents[data['id']]
                except:
                    data['textbook'] = ''
                if '教学过程' in file:
                    try:
                        data['tips'] = process_contents[data['id']]
                    except:
                        data['tips'] = ''
                # elif '学情分析' in file:
                #     try:
                #         data['tips'] = sta_contents[data['id']]
                #     except:
                        
                #         data['tips'] = ''
                # elif '教学评价' in file:
                #     data['tips'] = eval_contents[data['id']]
                item_list.append(data)
        return item_list


            
def get_mode(subject, lesson_info):
    if subject == '信息科技':
        os.path.join("/mnt/cfs/zengxiaoli/english_lesson_plan_generator/result/1022_mode",lesson_info+".json")
        try:
            with open(os.path.join("/mnt/cfs/zengxiaoli/english_lesson_plan_generator/result/1022_mode",lesson_info+".json"), 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data['mode']
        except:
            return '自定义'
    else:
        return random.choice(model_common_list[subject])


def get_all_json_files(directory,file_type = "json"):
    # 使用glob.glob递归搜索所有.json文件
    json_files = glob.glob(os.path.join(directory, '**', f'*.{file_type}'), recursive=True)
    return json_files

def model_lesson_result():
    result_path = "/mnt/cfs/zhengying/lesson_plan_generator_zy/eval_data"
    # model_name = ["claude3-sonnet", "gemini15-pro", "GPT4-FAST"]
    model_name = ["GLM-4"]
    sample_ids_path = "../data/sample_ids.json"
    sample_ids = read_json(sample_ids_path)
    
    for mn in model_name:
        # model_path = f"{result_path}/{mn}_1221"
        model_path = f"{result_path}/{mn}"

        subject_ids = []
        for subject in ["数学", "英语", "科学", "信息科技", "物理", "化学"]:
            for si in sample_ids[subject]:
                subject_ids.append(si["id"])
            print(f"process the {mn} {subject}")
            ms_path = f"{model_path}/{subject}"
            ms_file = get_all_json_files(ms_path)
            ms_list = {}
            for mf in ms_file:
                ms_data = read_json(mf)
                lesson_id = ms_data["id"]
                if lesson_id not in ms_list:
                    ms_list[lesson_id] = {}
                # if lesson_id in subject_ids:
                module = ms_data["module"]
                lesson_info = ms_data["lesson_info"]
                ms_list[lesson_id]["lesson_info"] =f"""{lesson_info}\n\n{ms_data["link"]}"""
                ms_list[lesson_id][module] = f"""{ms_data["response"]}"""
            
            ms_csv = [["model name", "id", "lesson_info", "response"]]
            for lid, value in ms_list.items():
                item_csv = [mn, lid, value["lesson_info"]]
                lesson_content = ""
                try:
                    for cp in ["教学内容分析", "学情分析", "教学目标", "教学重难点", "教学准备", "教学过程", "教学评价"]:
                        lesson_content += f"""{cp}\n{value[cp]}\n\n"""
                    item_csv.append(lesson_content)    
                    ms_csv.append(item_csv)
                except Exception as e:
                    print(f"error: {e}\n{lid}")
            if len(ms_csv) > 1:
                gen_file = pd.DataFrame(ms_csv)
                file_name = f"""{model_path}/{mn}_{subject}.csv"""
                gen_file.to_csv(file_name,index=False, header=False)
                print(f"save file as {file_name}")
                
def model_lesson_result_temp():
    result_path = "/mnt/cfs/zhengying/lesson_plan_generator_zy/eval_data"
    # model_name = ["claude3-sonnet", "gemini15-pro", "GPT4-FAST", "iFlytekSpark", "GLM-4", "ERNIE"]
    model_name = ["zxl_GPT4-FAST_0106"]
    sample_ids_path = "../data/sample_ids.json"
    sample_ids = read_json(sample_ids_path)
    sample_ids_temp_path = "../data/sample_ids_1224_eval.json"
    
    for mn in model_name:

        # model_path = f"{result_path}/{mn}_1221"
        model_path = f"{result_path}/{mn}"

        subject_ids = []
        for subject in ["数学", "英语", "科学", "信息科技", "物理", "化学"]:
            for si in sample_ids[subject]:
                subject_ids.append(si["id"])
            print(f"process the {mn} {subject}")
            ms_path = f"{model_path}/{subject}"
            ms_file = get_all_json_files(ms_path)
            ms_list = {}
            for mf in ms_file:
                ms_data = read_json(mf)
                lesson_id = ms_data["id"]
                if lesson_id not in ms_list and lesson_id in subject_ids:
                    ms_list[lesson_id] = {}
                if lesson_id in subject_ids:
                    module = ms_data["module"]
                    lesson_info = ms_data["lesson_info"]
                    ms_list[lesson_id]["lesson_info"] =f"""{lesson_info}\n\n{ms_data["link"]}"""
                    ms_list[lesson_id][module] = f"""{ms_data["response"]}"""
            with open(sample_ids_temp_path, "r") as f:
                sample_ids_temp = json.load(f)
            subject_ids_temp = {item['id']:['',''] for item in sample_ids_temp[subject]}
            ms_csv = [["model name", "id", "lesson_info", "response"]]
            for lid, value in ms_list.items():
                if lid not in subject_ids_temp: continue
                item_csv = [mn, lid, value["lesson_info"]]
                lesson_content = ""
                try:
                    for cp in ["教学内容分析", "学情分析", "教学目标", "教学重难点", "教学准备", "教学过程", "教学评价"]:
                        lesson_content += f"""{cp}\n{value[cp]}\n\n"""
                    subject_ids_temp[lid][0]=lesson_content
                    subject_ids_temp[lid][1]=value["lesson_info"]
                    
                except Exception as e:
                    print(f"error: {e}\n{lid}")
            for lid, value in subject_ids_temp.items():
                if value == [] :continue
                item_csv = [mn, lid, value[1]]
                item_csv.append(value[0])    
                ms_csv.append(item_csv)
            if len(ms_csv):
                gen_file = pd.DataFrame(ms_csv)
                file_name = f"""{model_path}/{mn}_{subject}_without_rag.csv"""
                gen_file.to_csv(file_name,index=False, header=False)
                print(f"save file as {file_name}")               

def get_previous_id(id_str):
    match = re.search(r'(\d+)$', id_str)
    if match:
        number = int(match.group(1))
        new_number = number - 1
        return re.sub(r'\d+$', str(new_number), id_str)
    else:
        return '-1'
    
def get_ok(unit_dir):
    obj_contents = {}
    key_contents = {}
    
    for root, dirs, files in os.walk(unit_dir):
        for file in files:
            if file.endswith('.json'):
                with open(os.path.join(root, file), 'r') as f:
                    data = json.load(f)
                    for item in data:
                        if item['module'] == '教学目标':
                            obj_contents[item['id']] = item['response']
                        elif item['module'] == '教学重难点':
                            key_contents[item['id']] = item['response']
    return obj_contents, key_contents

def create_single_test_data(data, key, key_value, save_path):
    data = [item for item in data if item[key] == key_value]
    save_path = save_path.replace('.json', f'_{key}_{key_value}.json')
    return data, save_path