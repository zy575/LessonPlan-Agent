import pandas as pd
import copy
import json

# 读取Excel文件
# model_infor = df.copy()
# model_list = model_infor['教学模式（新名称）']
# # model_list = set(model_list)
# model_lists = []
# for ml in model_list:
#     if ml not in model_list and isinstance(ml, str):
#         model_lists.append(ml)
# print(model_lists)
# model_infor['教学模式（新名称）'] = model_infor['教学模式（新名称）'].fillna(method='ffill')
# models_data = [['序号','教学模式','教学环节','模式简介','适用学段','适用学科']]

# n = 1
# print(len(model_lists))
# models_data = [['序号','教学模式','教学环节','模式简介','适用学段','适用学科']]

# for ml in model_lists:
#     # print('ml: ', ml)
#     for index, row in model_infor.iterrows():    
#         # print(row)
#         if row['教学模式（新名称）'] == ml:
#             if isinstance(row['适用学科'],str):
#                 row1 = n
#                 row2 = row['教学模式（新名称）']
#                 row3 = [row['教学环节']]
#                 row4 = row['模式简介']
#                 row5 = row['适用学段']
#                 row6 = row['适用学科']
#             else:
#                 row3.append(row['教学环节'])
#     mtemp = [row1, row2, row3, row4, row5, row6]
#     models_data.append(mtemp)
#     n += 1
# print(models_data)

# models_file = pd.DataFrame(models_data)
# file_name = f"./teaching_models_v2.csv"
# models_file.to_csv(file_name,index=False, header=False)

# models = {}
# for md in models_data[1:]:
#     if md[1] not in models:
#         temp={}
#         temp['教学环节'] = md[2]
#         temp['模式简介'] = md[3]
#         temp['适用学段'] = md[4]
#         temp['适用学科'] = md[5]
#         models[md[1]] = temp
# models
# teaching_models = models

# 教学模式

models_list = ['探究式教学', '讲授式教学', '协作式教学', '基于问题的教学', '自学——辅导教学', '案例式教学', '头脑风暴式教学', '项目式学习', '换位式教学', '讲座式教学', '支架式教学', 
 '以文献为导向的自我学习', '概念获得式教学', '启发式教学', '抛锚式教学', '运用几何画板讲授数学公理、定理', '“设问—导学”教学模式', '任务驱动式教学', '“问题－实验－探究”教学模式', 
 '激励——导学教学模式', '识、读、写三结合教学模式（211模式）', '低年级识字教学模式', '“随文识字”教学模式', '语文阅读课教学模式', '精加略教学模式', '古诗阅读教学模式', '作文教学模式', 
 '小学语文读写教学模式', '角色扮演教学模式', '以言语交际为中心的新授课教学模式', '以言语交际为中心的复习课教学模式', '基于资源支持的英语听说教学模式', '小学英语拓展听说教学模式', 
 '多媒体网络下英语“任务型”教学模式', '以言语交际为中心的巩固练习课教学模式', '图文归纳模式', '情景式教学', '辩论式教学', '研究型教学', '比较式教学', '单点式教学', '自定义']

#常用的
model_common_list = {
  "英语": ['探究式教学', '讲授式教学', '协作式教学', '基于问题的教学', '自学——辅导教学', '案例式教学', '头脑风暴式教学', '启发式教学', '任务驱动式教学', '以言语交际为中心的新授课教学模式', '小学英语拓展听说教学模式', '自定义'],
  "科学": ['探究式教学', '讲授式教学', '协作式教学', '基于问题的教学', '案例式教学', '头脑风暴式教学',  '任务驱动式教学', '“问题－实验－探究”教学模式'],
  "化学": ['探究式教学', '讲授式教学', '协作式教学', '基于问题的教学', '“问题－实验－探究”教学模式'],
  "物理": ['探究式教学', '讲授式教学', '协作式教学', '基于问题的教学', '“问题－实验－探究”教学模式'],
}

teach_model_path = "/mnt/cfs/zhengying/lesson_plan_generator_zy/data/teach_mode_time.json"
with open(teach_model_path, 'r', encoding='utf-8') as file:
    teach_model_time = json.load(file)

teaching_models = {'探究式教学': {'教学环节': ['情境创设，课程导入','分析问题，明确目标','动手实践，探究新知','课堂总结，建构概念','知识巩固，迁移应用'],
                  '模式简介': '探究式教学以问题解决为中心的，注重学生的独立活动，注重体验式教学，着眼于学生的思维能力的培养。',
                  '适用学段': '小学、初中、高中',
                  '适用学科': '通用'},
 '讲授式教学': {'教学环节': ['导入新课', '检查复习', '讲授新课', '巩固新课', '课堂总结', '布置作业'],
  '模式简介': '该模式以传授系统知识、培养基本技能为目标。其着眼点在于充分挖掘人的记忆力、推理能力与间接经验在掌握知识方面的作用，使学生比较快速有效地掌握更多的信息量。',
  '适用学段': '小学、初中、高中',
  '适用学科': '通用'},
 '协作式教学': {'教学环节': ['课程导入，明确主题',
   '围绕主题，明确问题',
   '小组协作，解决问题',
   '成果展示，交流汇报',
   '总结评价，优化方案'],
  '模式简介': '协作式教学模式是一种强调学生互相合作、参与和共同构建知识的教学方法。它强调学生在教学过程中的积极参与和合作，促进他们的自主学习和批判性思维能力的培养。',
  '适用学段': '小学、初中、高中',
  '适用学科': '通用'},
 '基于问题的教学': {'教学环节': ['创设情境，引出问题',
   '分析问题，明确目标',
   '实践探究，解决问题',
   '成果展示，经验交流',
   '评价反馈，归纳总结',
   '学以致用，巩固提升'],
  '模式简介': '基于问题的教学模式是一种以学生为中心的教学方式，教师通过提出问题来引导学生思考、探究和解决问题。这种教学模式强调学生的主动性和参与性，旨在激发学生的学习兴趣、培养解决问题的能力和促进深入理解知识。',
  '适用学段': '小学、初中、高中',
  '适用学科': '通用'},
 '自学——辅导教学': {'教学环节': ['告知学生目标', '自主学习', '讨论交流', '启发指导', '课堂总结', '练习巩固'],
  '模式简介': '该模式有助于发挥学生的主体性，以培养学生的学习能力为目标。 先让学生独立学习，然后根据学生的具体情况教师进行指导。重视学生在学习过程中试错的机会和价值，培养学生独立思考和学会学习的能力。',
  '适用学段': '小学、初中、高中',
  '适用学科': '通用'},
 '案例式教学': {'教学环节': ['复习导入，知识激活',
   '案例分析，提高认识',
   '总结反思，加深认识',
   '巩固练习，提高能力',
   '作业布置，加深理解'],
  '模式简介': '案例式教学模式遵循从个别到一般，从具体到抽象的人类认知规律。在教学中从一些范例分析入手感知原理与规律，并逐步提炼进行归纳总结，再进行迁移整合。',
  '适用学段': '小学、初中、高中',
  '适用学科': '通用'},
 '头脑风暴式教学': {'教学环节': ['导读，引入学习',
   '课程学习',
   '引出话题',
   '学生讨论交流',
   '教师讲解解惑',
   '总结反思',
   '巩固练习'],
  '模式简介': '头脑风暴指在规定的时间内，众多人围绕一个主题或问题，在不对别人的见解有任何批评和指责的前提下，尽量展开自己的想象思维、随意发表自己的见解，从而寻求问题解决策略的教学模式。头脑风暴式教学模式能够有助于学生对问题的深入思考，借助于群体智慧，对该知识领域有更全面的认识。',
  '适用学段': '小学、初中、高中',
  '适用学科': '通用'},
 '项目式学习': {'教学环节': ['情景导入，明确项目',
   '收集资料，制定方案',
   '头脑风暴，筛选方案',
   '小组协作，具体实施',
   '成果展示，经验分享',
   '评估反思，总结经验'],
  '模式简介': '学生以项目为中心，学生利用教学资源，进行独立探索和互动协作的学习，学生在完成项目的同时，获取相应的知识和问题解决能力。该模式能够为学生提供真实的实践情景，便于学习知识的迁移应用，以项目为中心的学习，能够促使学生主动探究、实践、应用，促进学生高阶认知水平的发展。',
  '适用学段': '小学、初中、高中',
  '适用学科': '通用'},
 '换位式教学': {'教学环节': ['布置“教学”内容', '成立“教学”小组', '引导学生备课', '学生讲课', '师生评议'],
  '模式简介': '“换位教学”，就是师生位置互换，让学生上讲台，扮演老师的角色，组织教学，进行授课活动；而老师则以学生的身份听课，实现师生角色位置互换。学生在教师引导下，自学理解教学内容，然后在课堂上阐述自己对所学知识的理解，以自己的亲身经历和阅历来体验知识，甚至启发别人。而老师的任务便是仔细聆听，大胆鼓励学生发表见解，并及时纠正错误的偏见和过激的思想，引导学生正确而多角度的理解教学内容，像学生一样发表自己的见解，把知识融合在互相的探讨之中。',
  '适用学段': '小学、初中、高中',
  '适用学科': '通用'},
 '讲座式教学': {'教学环节': ['教师分组，确定讲座主题', '小组分工，协作准备', '举行专题讲座', '提问答疑', '提交讲稿、报告'],
  '模式简介': '对于相对独立或者前沿的教学内容，通过讲座的形式，教师或学生做主题发言，然后集体讨论探讨，让学生通过自学解决自己所能解决的问题，而把教师的主要精力用于指导学生的学习方法，解决教学中的重点、难点，既能加深对学习主题的理解，又扩充了学生学习的知识领域。',
  '适用学段': '小学、初中、高中',
  '适用学科': '通用'},
 '支架式教学': {'教学环节': ['课程导入', '设置问题情境，提出问题', '独立探索，查阅参考资料', '讨论交流', '总结评价'],
  '模式简介': '支架式教学事先把复杂的学习任务加以分解，并为学习者建构对知识的理解提供一种概念框架（Conceptual Framework），以便于把学习者的理解逐步引向深入。支架式教学依据“最邻近发展区”所建立的脚手架，能够符合学生发展的需要，可以不停地把学生的智力从一个水平提升到另一个新的更高水平，真正做到使教学走在发展的前面。',
  '适用学段': '小学、初中、高中',
  '适用学科': '通用'},
 '以文献为导向的自我学习': {'教学环节': ['专题阐述', '分组自学', '文献研讨', '专题总结评价'],
  '模式简介': '采用自我学习的模式，学生成为学习的中心和主体，教师不再扮演权威的角色，而是努力为学生创设一个活泼的学习环境；教师为学生提供多种的教学资源，不仅丰富和扩大学生的信息量和知识面，而且还教给学生学习、思维、发现和解决问题的方法，并使其文献阅读能力和语言表达能力等研究素质得到提高。',
  '适用学段': '小学、初中、高中',
  '适用学科': '通用'},
 '概念获得式教学': {'教学环节': ['情景导入，明确教学目的',
   '呈现例子，分类归纳',
   '提出概念假设',
   '呈现例子，检验假设',
   '概括总结，形成概念',
   '反思概念化过程',
   '应用概念，巩固理解'],
  '模式简介': '概念获得式教学模式强调学生对知识的主动探索和构建，培养他们的思辨和分析能力，以及概念性知识的获取和应用。该模式的目标是使学习者通过体验所学概念的形成过程来培养他们的思维能力。',
  '适用学段': '小学、初中、高中',
  '适用学科': '数学、生物'},
 '启发式教学': {'教学环节': ['引出疑问', '课程学习', '提问与回答', '继续提问', '课堂总结', '巩固练习'],
  '模式简介': '启发式教学通过揭示学生头脑中已有的知识和经验中的矛盾因素，促使学生主动地去寻找解决问题的途径。运用启发式教学的关键在于教师的循循善诱，使学生在有限的知识基础上，利用大量典型范例，达到举一反三的效果。',
  '适用学段': '小学、初中、高中',
  '适用学科': '通用'},
 '抛锚式教学': {'教学环节': ['创设情境', '确定问题', '自主学习', '讨论交流', '效果评价'],
  '模式简介': '抛锚式教学的主要目的是使学生在一个完整、真实的问题背景中，产生学习的需要，并通过镶嵌式教学以及学习共同体中成员间的互动、交流，即合作学习，凭借自己的主动学习、生成学习，亲身体验从识别目标到提出和达到目标的全过程。',
  '适用学段': '小学、初中、高中',
  '适用学科': '数学、信息技术、科学'},
 '运用几何画板讲授数学公理、定理': {'教学环节': ['创设情境', '提出问题', '解决问题', '综合应用'],
  '模式简介': '该模式可以有效激发学生的学习积极性和投入度，给予学生实践和实验的机会，使他们能够像数学家一样进行探索、发现和归纳数学公理和定理方面的知识。',
  '适用学段': '小学、初中、高中',
  '适用学科': '数学'},
 '“设问—导学”教学模式': {'教学环节': ['教师提出问题', '学生探究问题', '引导学生解决问题', '归纳总结', '综合应用'],
  '模式简介': '"设问—导学"教学模式是一种教师引导学生主动探究知识的方法，学生通过提出问题来深入理解问题的背景和内涵，而教师则协助学生建立已有知识与新知识之间的关联，并教导学生学习的方法和技巧。',
  '适用学段': '小学、初中、高中',
  '适用学科': '科学、数学、信息技术'},
 '任务驱动式教学': {'教学环节': ['课程导入', '确定任务', '合作学习/自主探究', '交流汇报', '总结评价', '布置作业'],
  '模式简介': '任务驱动教学模式指的是，在教学活动中紧紧围绕一个共同的任务活动中心，在强烈的问题动机的驱动下，通过对学习资源的积极主动应用，进行自主探索或协作学习，并在完成既定任务的同时，引导学生产生一种学习实践活动。',
  '适用学段': '小学、初中、高中',
  '适用学科': '通用'},
 '“问题－实验－探究”教学模式': {'教学环节': ['创设情境，引出问题',
   '针对问题，作出假设',
   '设计实验，验证假设',
   '整理材料，归纳结论',
   '迁移应用，培养能力'],
  '模式简介': '该模式以问题为核心，调整学生学习活动的心理意向。 从实验中获取感性认识并联系旧知，形成完整的认识结构，以认知需求为原动力，培养学生的创造能力及探究未知世界的积极态度。',
  '适用学段': '小学、初中、高中',
  '适用学科': '科学、信息技术、物理、化学'},
 '激励——导学教学模式': {'教学环节': ['温故知新', '导趣激思', '导读激思', '导动激思', '导创激思', '答疑反馈'],
  '模式简介': '该模式利用导阅、导趣、导思、导动、导创等鼓励性方法激励学生的学习。导阅即根据不同教学内容要求，设计导读方法，强调综合分析能力，增强学生的阅读理解、应用能力；导趣即通过师生情感交流、实验、联系生活、生产应用、巧用化学史等方法激发学生学习兴趣；通过引导联想、从实验出发进行探索思维、联系生活等激发学生思考；多给学生创造实验机会，让他们从动手中思考、从动手中领会、应用化学知识；导创即给学生创造的机会，让他们多向思维，从设计实验、应用化学知识中体验创造的乐趣。',
  '适用学段': '小学、初中、高中',
  '适用学科': '化学、物理、科学、信息技术、数学'},
 '识、读、写三结合教学模式（211模式）': {'教学环节': ['新知教学', '拓展阅读', '写作表达'],
  '模式简介': '教学以教师指导为主导，学生的自主学习为主体，优化教学结构。按教师讲授、拓展阅读、书写练笔分配课时；比例为 2：1：1。按照课堂时间的划分，前20分钟达到课文教学目标的基本要求，主要以教师教学活动为主导。后20分钟达到巩固、深化、拓展对课文教学目标的要求，以学生活动为主体开展教学。',
  '适用学段': '小学、初中、高中',
  '适用学科': '语文'},
 '低年级识字教学模式': {'教学环节': ['引入新课', '识字教学', '写字教学', '扩展阅读', '写作表达'],
  '模式简介': '识字课教学模式以学生识字为主，通过自主探究、合作学习等方式，学生熟练掌握常用字，作为读写的基础。',
  '适用学段': '小学',
  '适用学科': '语文'},
 '“随文识字”教学模式': {'教学环节': ['激情引趣、释题识字',
   '初读课文、读准字音',
   '细读课文，理解字义',
   '分析字形、编码书写',
   '上机验证，多种训练'],
  '模式简介': '“随文识字”教学模式是一种以文本为基础的识字教学方法，旨在通过学习文本来提高学生的识字能力和阅读理解能力。该教学模式注重将识字与语境相结合，让学生在实际阅读中逐步积累和运用词汇。',
  '适用学段': '小学',
  '适用学科': '语文'},
 '语文阅读课教学模式': {'教学环节': ['创设情境，激发兴趣',
   '课文品读，感受新知',
   '拓展阅读，知识延伸',
   '知识应用，写作训练',
   '评价反馈，修正完善'],
  '模式简介': '语文阅读课教学模式旨在通过创设情境、课文品读、拓展阅读、知识应用和评价反馈等环节，培养学生的阅读能力、理解能力和写作能力。通过引发学生的兴趣，帮助他们深入理解课文内容，扩展知识面并将所学知识应用到写作中，该教学模式能够全面发展学生的语文素养。',
  '适用学段': '小学、初中、高中',
  '适用学科': '语文'},
 '精加略教学模式': {'教学环节': ['课程导入', '确定任务', '精读课文', '总结评价', '略读课文'],
  '模式简介': '精加略教学模式，即把有关连的两篇文章（一篇精读、一篇略读）结合在一起进行学习。中高年级语文教学的重心由识字为主过渡到阅读和写作应用为主，注重学生学习能力的培养，强调识字、阅读、写作三位一体。',
  '适用学段': '小学、初中、高中',
  '适用学科': '语文'},
 '古诗阅读教学模式': {'教学环节': ['熟知诗人，明晓题意', '理解诗意，体会诗情', '扩展阅读，知识迁移', '对照比较，知识总结'],
  '模式简介': '该模式注重学生对古诗的感知和体验，通过扩展阅读和对照比较，学生能够进一步拓展对古诗的感知和体验，从而更好地欣赏和理解古诗的美。',
  '适用学段': '小学、初中、高中',
  '适用学科': '语文'},
 '作文教学模式': {'教学环节': ['入境明题', '自主阅读', '总结技巧', '写作实践', '评议修改'],
  '模式简介': '作文教学模式是通过系统化的教学环节，从题目理解到写作实践，培养学生的写作技能。这个模式注重学生的自主学习、技巧积累、实践和反馈，旨在帮助学生成为有表达能力、有思考深度的文本创作者，提高他们在语言表达和写作方面的综合素养。',
  '适用学段': '小学、初中、高中',
  '适用学科': '语文'},
 '小学语文读写教学模式': {'教学环节': ['创设情境，激发兴趣',
   '课文品读，感受新知',
   '拓展阅读，知识延伸',
   '师生评说，交流促进',
   '知识应用，文章写作'],
  '模式简介': '小学语文读写教学模式通过有计划、有步骤的教学环节，全面培养学生的阅读理解、写作能力，同时通过兴趣激发和互动交流促进学习。该模式旨在培养全面的语文素养，使学生能够在语文领域中取得更好的学术成绩，并培养他们的思维和表达能力，以便更好地应对未来的学习和生活挑战。',
  '适用学段': '小学',
  '适用学科': '语文'},
 '角色扮演教学模式': {'教学环节': ['活动概述，任务说明',
   '角色分工，表演准备',
   '角色扮演，内容演绎',
   '自我与同伴评析',
   '教师总结'],
  '模式简介': '角色扮演模式的学习属于情境学习，孩子站在所扮演角色的角度来体验、思考，从而构建起新的理解和知识并培养生活必备的能力。它是一种以发展孩子为本，把创新精神的培养置于最重要地位的学习方式，整个教学过程始终渗透着师与生、生与生之间的交流合作,体现教师的主导,学生的主体地位。',
  '适用学段': '小学、初中、高中',
  '适用学科': '语文'},
 '以言语交际为中心的新授课教学模式': {'教学环节': ['活动激趣，引入新知',
   '听读新知，纵向拓展',
   '情景交际，应用新知',
   '扩展听读，语境感知',
   '迁移练习，交际应用'],
  '模式简介': '所谓新授，通常是指初次学习本单元的主题词汇、重点句型、主题故事等。一般课本上落实的基本教学目标是能够初步认知、掌握新词汇的音和义，并利用相关句型，能够围绕这些新词汇进行简单的对话听说。而在本模式下，除了掌握课本上要求的主题词汇，还要结合本主题的知识网络，或对主题词汇进行纵向拓展，或对相关的主题句型进行更为灵活的变式应用。',
  '适用学段': '小学、初中、高中',
  '适用学科': '英语'},
 '以言语交际为中心的复习课教学模式': {'教学环节': ['活动激趣，复习旧知',
   '语体引入，横向拓展',
   '情景交际，应用新知',
   '扩展听读，语境感知',
   '迁移练习，交际应用'],
  '模式简介': '所谓复习，也是针对本单元主题词汇与主题句型而言，单元复习课一般是针对一个单元较为靠后的课时而言，在这些课时中，要求掌握的本单元主题词汇或相关句型已经在前面课时中学习完毕，教材内容主要是和主题相关的相对较为复杂的语言材料如故事等，在这些语言材料中包含有本单元要求掌握的句型或单词，从而实现对这些词汇和句型的复习和巩固。',
  '适用学段': '小学、初中、高中',
  '适用学科': '英语'},
 '基于资源支持的英语听说教学模式': {'教学环节': ['创新识记词汇',
   '听读对话，学习新知',
   '角色扮演，表演故事',
   '改编故事，创新拓展',
   '展示评价，总结反思'],
  '模式简介': '基于资源支持的英语听说教学模式的核心理念是通过多样化的教学环节，利用丰富的资源来提高学生的英语听说能力。这个模式注重学生的互动参与、创造性思维和实际运用，旨在培养学生全面的语言技能和综合素质，使他们能够在真实生活中自信地使用英语。',
  '适用学段': '小学、初中、高中',
  '适用学科': '英语'},
 '小学英语拓展听说教学模式': {'教学环节': ['活动激趣，固旧引新',
   '听读示范，拓学词句',
   '唱背歌谣，对说会话',
   '借助网络，自主听读',
   '编演故事，灵活运用'],
  '模式简介': '小学英语拓展听说教学模式注重活动性、互动性和个性化的教学方法，旨在激发学生的学习兴趣，促进学生在愉快的学习氛围中积极参与，提高他们的听力和口语能力。',
  '适用学段': '小学',
  '适用学科': '英语'},
 '多媒体网络下英语“任务型”教学模式': {'教学环节': ['任务呈现明确目标',
   '人机交互，自主学习',
   '协作学习，创新实践',
   '完成任务，综合发展'],
  '模式简介': '多媒体网络下英语“任务型”教学模式强调学生的主动参与、自主学习、协作合作和实际应用。它不仅培养学生的语言技能，还注重了学生的综合素质和创新能力的培养，以适应现代社会对多方面能力的需求。此模式借助现代技术和互联网资源，为学生提供了更灵活、富有趣味和有挑战性的学习机会。',
  '适用学段': '小学、初中、高中',
  '适用学科': '英语'},
 '以言语交际为中心的巩固练习课教学模式': {'教学环节': ['创设情境，词句复习',
   '听写结合，强化训练',
   '师生互动，合理评价',
   '拓展听读，丰富旧知',
   '创设情境，学生交际',
   '灵活运用，写作训练'],
  '模式简介': '巩固课（练习课）是以练习、巩固新授课所学知识为主，达到让学生能够熟练掌握的目的。教师可以利用电脑、投影、手持式设备等信息技术手段作为情景创设工具，播放声音、动画，呈现文字，图片等；可以作为学生进行自我检测的工具，提供针对某些知识点的练习、英语游戏以及相应反馈；可以作为学生自主学习的工具，提供给学生丰富的英语听读资源，并可以随时录音、跟读对比，便于学生及时发现并改正自己的发音问题。',
  '适用学段': '小学、初中、高中',
  '适用学科': '英语'},
 '图文归纳模式': {'教学环节': ['教师选择一幅图画',
   '学生研究图画，辨认图画中事物',
   '老师读写英文单词，用线连接单词和图中事物',
   '学生听、跟读、拼写单词',
   '探究单词特点，进行分类',
   '学生反复朗读、拼写看图识字图表',
   '教师引导学生思考图中信息，为图设计标题',
   '学生用图中的词汇造一个句子或多个句子',
   '教师用标准的英语句法写出学生造的句子',
   '学生探究句子结构，并给句子分类',
   '教师从中选出代表性的句子组成示范段落',
   '学生练习写作段落或听写段落'],
  '模式简介': '图文归纳模式（Picture-word Inductive Model）就是专门为小学初学者和超龄初学者以及处于阅读低级阶段的学生而设计的一种探究型的教学模式。该模式基于对儿童语言自然习得过程的研究，将图片中的事物通过连线与单词对应起来，构成可视词汇，直观而方便。这样就把语言的学习和具体场景结合起来，协助学生主动探究语言的使用规律，从本质上提高学生的读写能力。\n图文归纳法的主要原则是不断充实学习者的词汇库和句法形式，避免脱离语境教学词汇。图文归纳法的教学通常是从一张图片开始，通过辨别物品、描述活动、归纳特征等步骤，把词汇与图片中的事物联系起来，并在具体语境中不断重复目标词汇，加强词汇在口语和书面语中的使用频率。图文归纳法使学生的探究周期结构化，每张图片的学习一般持续2～6周，教师根据内容难易程度控制时间，环环相扣，循环推进。',
  '适用学段': '小学',
  '适用学科': '英语'},
 '情景式教学': {'教学环节': ['设置问题情境，确立实验项目',
   '小组分配',
   '查找资料',
   '设计实验方案',
   '体验模拟',
   '教师点评',
   '提交体验报告'],
  '模式简介': '应用情境教学法，设置与教学内容相关的情境，将教学内容理论知识和实践技能结合起来，模拟真实场景，通过学生间相互合作和协调，使学生真正成为课堂教学中的主体和自我发展的主体，从而科学有效地解决综合性实验教学中的问题，为理论教学和实践教学的结合提供良好的平台。',
  '适用学段': '小学、初中、高中',
  '适用学科': '通用'},
 '辩论式教学': {'教学环节': ['导读，引入学习', '课程学习', '引出辩题', '分组', '查阅整理资料', '辩论', '辩论总结'],
  '模式简介': '辩论式学习的特点是正反双方的任务始终是用事实和逻辑推理阐明自己的观点，抓住对方论点、论据中的问题，力图驳倒对方。辩论式教学的特点决定了它是培养学生思维的敏捷性、批判性、逻辑性、语言的组织与表达能力以及心理素质的稳定性的最佳学习形式之一，是展示学生多方面能力、素质的重要途径。',
  '适用学段': '小学、初中、高中',
  '适用学科': '通用'},
 '研究型教学': {'教学环节': ['教师提出课题', '分组', '深入研究', '集体研讨', '完成报告', '评价'],
  '模式简介': '在教学的过程中，教师把研究的项目及方向和教学课程相结合，在教师的指导下，通过阅读文献或课题研究，在学习中研究、在研究中学习，遇到了问题深入分析研究，用已有知识学习求解问题所需要的知识，使学习和研究成为一个互动的过程。在研讨中积累知识、培养能力和锻炼思维。',
  '适用学段': '小学、初中、高中',
  '适用学科': '通用'},
 '比较式教学': {'教学环节': ['导言引入', '课程学习', '作比较', '比较反馈'],
  '模式简介': '比较是人们认识、鉴别事物的一种方法，也是一种有效的教学方法。比较教学表现在课程中，就是把两个或两个以上的相似的概念结合在一起进行教学，找出其中相同点和不同点，通过比较鉴别，使学生比较全面地掌握知识和技能的一种教学方法。运用比较教学，可以培养学生分析事物、判断思考、求同辨异的创造能力，可以促使学生对概念知识有进一步的理解和掌握，培养学生的理解能力、鉴赏能力，从而提高课堂教学效率。',
  '适用学段': '小学、初中、高中',
  '适用学科': '通用'},
 '单点式教学': {'教学环节': ['调查，确定层次', '分组', '小组学习', '发布作品', '评价'],
  '模式简介': '将教学内容以相关岗位典型工作任务和就业标准为目标，进行有效分解和重新组合，划分出若干个单元模块，学生可以根据自己的兴趣和能力选择部分或全部学习单元，教师因材施教，进行个性化的教学，不求面面俱到，但求一技精通，最终实现学生各自的学习目标。',
  '适用学段': '小学、初中、高中',
  '适用学科': '通用'},
 '自定义': {'教学环节': ['课程导入', '新课学习', '巩固练习', '课堂总结'],
  '模式简介': '您可以根据自身需要自定义本节课的教学环节',
  '适用学段': '小学、初中、高中',
  '适用学科': '通用'}}

# 教学环节示范
##科学
science_example = '''
教科版小学科学一年级上册第二单元《比较与测量》第 6 课《做一个测量纸带》教学设计
教学过程
一、聚 焦 
1.情境导入
通过播放小马过河的动画视频，设置教学情境，牛伯伯、小松鼠、小马用自己身体测量河水深浅，结果都不一样，引导学生思考：用不同的物体来测量，测量结果不能比较怎么办？

2.选择测量的标准物
课件出示回形针、小棒、小立方体，引导学生选择其中一种物体作为测量标准物，同时鼓励学生说出理由。

二、探索
活动一：制作测量纸带
提出问题：我们该怎样做测量纸带？
介绍制作测量纸带的实验材料。
介绍制作测量纸带的步骤和注意事项：每段纸带首尾要相连；粘贴时，纸带要连成直线；用数字做标记。
视频演示测量纸带的制作过程。
强调：制作测量纸带时应注意细节：起点必须从“0”开始。

活动二：用测量纸带测量书的长度和宽度
介绍测量书本的长度和宽度时应该注意：纸带的起点——“0”刻度线要与书本边长的边缘起点对齐，纸带与书本边长的另一端重合的位置就是终点。
强调：先预测书本的长度，再用测量纸带来测量，最后在实验记录单上记录数据。
视频演示测量书的长度和宽度的过程。
记录并比较测量数据。

活动三：用测量纸带测量小桶一圈的长度
视频演示用测量纸带测量小桶底部边沿一圈的长度。
强调用测量纸带测量小桶底部一圈的长度时应注意的问题。
记录数据，分析对比预测结果和测量结果，感受测量纸带的准确性。
……
'''


component_json = {
        "module_name": "教学目标",
        "module_description": [
            {
                "num": "1",
                "title": "知识目标",
                "content": "学生能够理解并掌握圆的基本概念，知道圆心、半径、直径、弦、圆周等基本概念，并能够画出一个标准的圆。"
            },
            {
                "num": "2",
                "title": "能力目标",
                "content": "培养学生的空间想象能力和几何图形的绘制能力。"
            },
            {
                "num": "3",
                "title": "情感目标",
                "content": "通过学习圆的基本概念，让学生感受数学的严谨和几何图形的美。"
            }
        ]
    }
# component_example = '''
# <h1>知识与技能</h1>
# 学生能够理解并掌握圆的基本概念，知道圆心、半径、直径、弦、圆周等基本概念，并能够画出一个标准的圆。
# <h1>过程与方法</h1>
# 培养学生的空间想象能力和几何图形的绘制能力。
# <h1>情感态度价值观</h1>
# 通过学习圆的基本概念，让学生感受数学的严谨和几何图形的美。
# '''

component_example = '''
<h1>title1</h1>
title1的内容
<h1>title2</h1>
title2的内容
<h1>title3</h1>
title3的内容
'''

teach_assess = '''
<h1>学生评估</h1>
学生评估的内容
<h1>课堂评估</h1>
课堂评估的内容
<h1>教师评估</h1>
教师评估的内容
'''

stu_analysis = '''
<h1>前置知识点</h1>
前置知识点的内容
<h1>本节知识点</h1>
本节知识点的内容
<h1>学生发展水平</h1>
学生发展水平的内容
'''
keyPoint_example = '''
<h1>教学重点</h1>
教学重点的内容
<h1>教学难点</h1>
教学难点的内容
'''

materials_example = '''
<h1>教具</h1>
课件、直尺
<h1>教学活动</h1>
用于课堂游戏的卡片
'''

act1='''
师：（带领学生观察教室里的植物）"你们看，这些植物是怎么长大的？"
生：（学生观察并提出自己的看法）"它们需要水和阳光。"
师：（提问）"那么，没有水和阳光，植物会怎么样呢？"
生：（学生思考并提出猜想）"可能会枯萎或者死掉。"
活动意图：通过观察植物，引发学生对植物生长所需条件的思考，引出教学问题。'''

act2='''
师：（讲述关于植物的生命力的故事，如豆种的生长故事）"你们听说过这个故事吗？你们从故事中学到了什么？"
生：（听故事并回答问题）"植物是有生命的，需要像我们一样呼吸、吸取营养。"
活动意图：通过故事，使学生进一步明确植物是有生命的这一概念。'''

act3='''
师：（指导小组讨论）"你们觉得，植物为什么需要水和阳光才能生长？如果我们设计一个实验来验证我们的想法，应该怎么做呢？"
生：（小组内部讨论并提出假设和实验设计）"我们认为植物需要水和阳光是因为……如果设计实验，我们可以……"
活动意图：引导学生就植物生长需要水和阳光这一问题进行思考和猜想，让他们理解科学的探究过程。
'''

# process_example = f'''
# <h1>创设情境，引出问题</h1>
# <h2>植物观察与思考</h2>
# {act1}

# <h2>故事启示</h2>
# {act2}

# <h1>针对问题，作出假设</h1>
# <h2>小组讨论</h2>
# ……
# '''

process_example = f'''
<h1>一、创设情境，引出问题（5min）</h1>
<h2>1.植物观察与思考</h2>
……
<h2>2.故事启示</h2>
……
<h1>二、针对问题，作出假设（10min）</h1>
<h2>1.小组讨论</h2>
……
<h2>……</h2>
……
<h2>……</h2>
'''



process_json = {
        "module_name": "教学过程",
        "module_description": [
            {
                "num": "1",
                "title": "一、创设情境，引出问题",
                "time": "5min",
                "content": [
                    {
                        "num": "1",
                        "title": "植物观察与思考",
                        "content": f"{act1}"
                    },
                    {
                        "num": "2",
                        "title": "故事启示",
                        "content": f"{act2}"
                    }
                ]
            },
            {
                "num": "2",
                "title": "二、针对问题，作出假设",
                "time": "10min",
                "content": [
                    {
                        "num": "1",
                        "title": "小组讨论",
                        "content": f"{act3}"
                    }
                ]
            }
        ]
    }


# activity = '''
# <h2>(教学活动1)</h2>
# 师：(老师的活动及讲话1)
# 生：(学生的活动及讲话1)
# 师：(老师的活动及讲话2)
# 生：(学生的活动及讲话2)
# ……
# 师：(老师的活动及讲话n)
# 生：(学生的活动及讲话n)
# 活动意图：

# <h2>(教学活动2)</h2>
# 师：(老师的活动及讲话1)
# 生：(学生的活动及讲话1)
# ……

# <h2>(教学活动n)</h2>
# **括号()和里面的文字都换成具体的内容**
# '''

activity = '''
师：(老师的活动及讲话1)
生：(学生的活动及讲话1)
师：(老师的活动及讲话2)
生：(学生的活动及讲话2)
……
师：(老师的活动及讲话n)
生：(学生的活动及讲话n)
活动意图：
**括号()和里面的文字都换成具体的内容**
'''