# %%
import os 
import pandas as pd
import math
from sklearn.metrics import cohen_kappa_score
import numpy as np
subject = ["math", "english", "chemistry", "science", "it"]
columns_to_drop = ['course information', 'textbook content','response','lesson_info','model name','60']
root_dir = './result/consistent'
save_dir = './result/consistent_detail'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
subject_rst = {}
model_dict = {}
model_dict_consistent = {}
subject_list = []
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if not  file.endswith('.xlsx'): continue
        subject_temp = root.split('/')[-1]
        model_name = file.split('_')[0]
        if subject_temp not in subject_rst:
            subject_rst[subject_temp] = {}
        file_name = file.split('.')[0]
        if file_name in subject_rst[subject_temp]:
            subject_rst[subject_temp][file_name] = None
        sheets_dict = {}
        file_path = os.path.join(root, file)
        excel_file = pd.ExcelFile(file_path)
        kappa_list = []
        sheet_name_list = excel_file.sheet_names
        for sheet_name in sheet_name_list:
            sheet_name_excel = pd.read_excel(file_path, sheet_name=sheet_name)
            
                # sheet_name_excel = sheet_name_excel.drop(columns=['lesson_info','response'])
            for col in columns_to_drop:
                if col in sheet_name_excel.columns:
                    sheet_name_excel = sheet_name_excel.drop(columns=[col])
            sheet_name_excel.fillna(0, inplace=True)
            # sheet_name_excel = sheet_name_excel
            # if sheet_name == '刘润':
            if  ('sigir' in root and ((subject_temp == 'english') or (subject_temp == 'science'))):
                df_transposed = sheet_name_excel
                # print(df_transposed)
            else:
                df_transposed = sheet_name_excel.transpose().reset_index()
                # 设置新的列名
                df_transposed.columns = df_transposed.iloc[0]
                df_transposed = df_transposed.drop(0).reset_index(drop=True)
            sheets_name_dict = df_transposed.to_dict(orient='list')
            # print(sheets_name_dict)
            # else:
            # sheets_name_dict = sheet_name_excel.to_dict(orient='records')
            sheets_dict[sheet_name] = {}
            for key, value in sheets_name_dict.items():
                # print('item', key, value)
                key = str(key)
                try:
                    key_int = int(key)
                except ValueError:
                    key_int = None
                    # key_int = key
                if ((key_int is not None and 1 <= key_int <= 50)):
                    if key not in sheets_dict[sheet_name]:
                        sheets_dict[sheet_name][key] = value
                    # sheets_dict[sheet_name][key].append(value)
            
        # print(sheets_dict)
        kappa_mean_list = []
        new_data = []
        # print(sheets_dict[sheet_name_list[0]])
        result_sum = []
        result_len = 0
        for key, value in sheets_dict[sheet_name_list[0]].items():
            # print(key)
            # print(value, value2, value3)
            # value = math.floor(float(value)) if isinstance(value, str) else math.floor(value)
            value2 = sheets_dict[sheet_name_list[1]][key]
            value3 = sheets_dict[sheet_name_list[2]][key]
            value = [math.floor(float(i)) for i in value]
            value2 = [math.floor(float(i)) for i in value2]
            value3 = [math.floor(float(i)) for i in value3]
            print(value, value2, value3)

            kappa_12 = cohen_kappa_score(value, value2)
            kappa_13 = cohen_kappa_score(value, value3)
            kappa_23 = cohen_kappa_score(value2, value3)
            if np.isnan([kappa_12]).any():
                kappa_12 = 1
            if np.isnan([kappa_13]).any():
                kappa_13 = 1
            if np.isnan([kappa_23]).any():
                kappa_23 = 1
            kappa_mean_list.append(np.mean([kappa_12, kappa_13, kappa_23]))
            # print(subject_temp,file_name,key, kappa_12, kappa_13, kappa_23, np.mean([kappa_12, kappa_13, kappa_23]))
            temp_list = [subject_temp, file_name, key, kappa_12, kappa_13, kappa_23, np.mean([kappa_12, kappa_13, kappa_23])]
            result_sum += value+value2+value3
            new_data.append(temp_list)
            # result_len += len(value+value2+value3)
        result_sum = [float(x) for x in result_sum]
        new_df = pd.DataFrame(new_data, columns=['subject', 'file_name', 'id', 'kappa_12', 'kappa_13', 'kappa_23', 'kappa_mean'])
        new_df.to_csv(f'{save_dir}/'+subject_temp+file_name+'.csv', index=False)
        if model_name not in model_dict:
            model_dict[model_name] = {}
        if subject_temp not in model_dict[model_name]:
            model_dict[model_name][subject_temp] = []
        if subject_temp not in subject_list:
            subject_list.append(subject_temp)
        model_dict[model_name][subject_temp].append(np.sum(result_sum)/len(result_sum))
        if model_name not in model_dict_consistent:
            model_dict_consistent[model_name] = {}
        if subject_temp not in model_dict_consistent[model_name]:
            model_dict_consistent[model_name][subject_temp] = []
        model_dict_consistent[model_name][subject_temp].append(np.mean(kappa_mean_list))
        model_dict[model_name][subject_temp].append(np.sum(result_sum)/len(result_sum))
        
        print(f"avg:{subject_temp}_{file}_consistent:{np.mean(kappa_mean_list)}")
        
new_data = []    
for key, value in model_dict.items():
    # for subject in model_dict[key]:
    # print(key,value)
    temp = [key]
    for subject in subject_list:
        try:
            temp.append(round(float(value[subject][0]),3))
        except:
            temp.append(0)
            
        # print(temp)
    new_data.append(temp)
# print(new_data[0])
df = pd.DataFrame(new_data, columns=['model_name']+subject_list)
df.to_csv(f"{save_dir}/result.csv", index=False)       
            
new_data = []    
for key, value in model_dict_consistent.items():
    # for subject in model_dict[key]:
    # print(key,value)
    temp = [key]
    for subject in subject_list:
        try:
            temp.append(round(float(value[subject][0]),3))
        except:
            temp.append(0)
            
        # print(temp)
    new_data.append(temp)
# print(new_data[0])
df = pd.DataFrame(new_data, columns=['model_name']+subject_list)
df.to_csv(f"{save_dir}/result_consistent.csv", index=False)              
# sheets_dict                
            








# %%



