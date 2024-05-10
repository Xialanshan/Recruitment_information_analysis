# -*- coding: utf-8 -*-
import mysql.connector
from pypinyin import lazy_pinyin
import pandas as pd
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
import cv2
import os


plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False                  # 解决负号显示为方块的问题


"""创建表类: 从数据库中导入表的信息,并做处理"""
class table_extract():
    """初始化:城市和职业名称"""
    def __init__(self,city:str,position:str):      
        self.city = city
        self.position = position

    """表的命名"""
    def name(self):         
        city_pinyin = lazy_pinyin(self.city)
        city_name = ''.join(city_pinyin)
        position_pinyin = lazy_pinyin(self.position)
        position_name = ''.join(position_pinyin)
        return city_name, position_name

    """判断该表是否存在"""
    def is_table_exists(self):    
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12041111Xx',
            database='bosszhipin')  
        city_name,position_name = self.name()
        cursor = db.cursor()
        cursor.execute("SHOW TABLES LIKE %s", (f'{city_name}_{position_name}',))
        result = cursor.fetchone()
        cursor.close()
        db.close()
        if result:
            return True
        else:
            return False
    
    """导入表的信息"""
    def import_table_info(self):
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12041111Xx',
            database='bosszhipin'
            )    
        if self.is_table_exists():
            city_name,position_name = self.name()
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM {city_name}_{position_name}")    # 查询表结构信息
            table_info = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]              # 将数据转换为 DataFrame
            df = pd.DataFrame(table_info, columns=columns)
            df = self.delete_index(df,'salary','天')
            df = self.delete_index(df,'salary','元')
            df = self.delete_index(df,'title','实习')
        else:
            return False
        cursor.close()
        db.close()
        return df   # 返回dataframe结构的表数据
    
    """删除属性包含指定关键词的条目"""
    def delete_index(self, df, column:str, keyword:str):         
        rows_to_delete = df[df[column].str.contains(keyword)].index
        df.drop(rows_to_delete, inplace=True)
        return df
    
    """处理薪资一栏"""
    def salary_process(self,salary:str):
        numbers = re.findall(r'\d+', salary)
        if len(numbers) == 1:
            aver_salary = int(numbers[0])*1000
        elif len(numbers) == 2:
            aver_salary = sum(map(int, numbers)) / len(numbers) *1000
        # 将提取的数字转换为整数并计算平均值
        else:
            numbers = [int(num) for num in numbers]
            aver_salary = (numbers[0]+numbers[1])/2*numbers[2]/12*1000
        return aver_salary
    
    """输出该职业在该城市的平均薪资"""
    def salary_print(self):
        df = self.import_table_info()
        df['salary_pro'] = df['salary'].apply(self.salary_process)
        average_salary = round(df['salary_pro'].mean())
        education_mean = round(df.groupby('education')['salary_pro'].mean()).sort_values(ascending=True)
        experience_mean = round(df.groupby('experience')['salary_pro'].mean()).sort_values(ascending=True)
        company_mean = round(df.groupby('company_size')['salary_pro'].mean()).sort_values(ascending=True)
        return average_salary,education_mean,experience_mean,company_mean

    """散点图"""
    # 1. 学历和薪资的散点图
    # 2. 工作经验和薪资的散点图
    # 3. 公司大小和薪资的散点图
    def scatter_diagram(self):
        """学历和薪资的散点图"""
        plt.figure(1)               
        df = self.import_table_info()
        df['salary_pro'] = df['salary'].apply(self.salary_process)
        unique_education = df['education'].unique()  
        label_indices = np.arange(len(unique_education))                        # 创建每个分类变量的索引
        label_index_mapping = dict(zip(unique_education, label_indices))        # 为每个唯一标签分配相应的索引
        indices = df['education'].map(label_index_mapping)                      # 获取每个标签的索引
        plt.scatter(df['salary_pro'],indices,s=3,c=df['salary_pro'],cmap='cividis')   
        plt.yticks(label_indices, unique_education,fontsize=7)
        plt.xticks(fontsize=7)                                    
        plt.title('Scatter diagram between salary and eduction',fontsize = 12)
        plt.xlabel('Salary',fontsize=10)
        plt.ylabel('Educational Requirements', fontsize=10)

        """工作经验和薪资的散点图"""
        plt.figure(2)
        df = self.import_table_info()
        df['salary_pro'] = df['salary'].apply(self.salary_process)
        unique_experience = df['experience'].unique()  
        label_indices = np.arange(len(unique_experience))                        # 创建每个分类变量的索引
        label_index_mapping = dict(zip(unique_experience, label_indices))        # 为每个唯一标签分配相应的索引
        indices = df['experience'].map(label_index_mapping)                      # 获取每个标签的索引
        plt.scatter(df['salary_pro'],indices,s=3,c=df['salary_pro'],cmap='cool')                               
        plt.yticks(label_indices, unique_experience,fontsize=7)
        plt.xticks(fontsize=7)                                  
        plt.title('Scatter diagram between salary and experience',fontsize = 12)
        plt.xlabel('Salary',fontsize=10)
        plt.ylabel('Experience Requirements', fontsize=10)

        """公司大小和薪资的散点图"""
        plt.figure(3)
        df = self.import_table_info()
        df['salary_pro'] = df['salary'].apply(self.salary_process)
        unique_company = df['company_size'].unique()  
        label_indices = np.arange(len(unique_company))                        # 创建每个分类变量的索引
        label_index_mapping = dict(zip(unique_company, label_indices))        # 为每个唯一标签分配相应的索引
        indices = df['company_size'].map(label_index_mapping)                      # 获取每个标签的索引
        plt.scatter(df['salary_pro'],indices,s=3,c=df['salary_pro'],cmap='tab10')                               
        plt.yticks(label_indices, unique_company,fontsize=5)
        plt.xticks(fontsize=5)                                          
        plt.title('Scatter diagram between salary and company size',fontsize = 10)
        plt.xlabel('Salary',fontsize=8)
        plt.ylabel('Company Size', fontsize=8)
        plt.show()

        
    """柱形图和折线图"""
    # 1. 学历和薪资(平均值)的横向柱形图
    # 2. 工作经验和薪资(平均值)的竖向柱形图
    # 3. 公司大小和薪资(平均值)的折线图
    def line_chart(self):
        average_salary,education_mean,experience_mean,company_mean = self.salary_print()
        """学历和薪资(平均值)的横向柱形图"""
        plt.figure(4)
        plt.barh(education_mean.index, education_mean.values, color='khaki', height=0.35)
        for i in range(len(education_mean.values)):
            plt.text(education_mean.values[i], i, round(education_mean.values[i]), ha='center', va='center', fontsize=8)
        plt.title('The relationship between education and average salary',fontsize = 12)
        plt.ylabel('Education',fontsize=10)
        plt.xlabel('Average Salary',fontsize=10)
        plt.xticks(fontsize=7)
        plt.yticks(fontsize=7)

        """工作经验和薪资(平均值)的竖向柱形图"""
        plt.figure(5)
        plt.bar(experience_mean.index, experience_mean.values, color='cornflowerblue', width=0.5)
        for i in range(len(experience_mean.index)):
            plt.text(experience_mean.index[i], experience_mean.values[i], round(experience_mean.values[i]), ha='center', va='bottom', fontsize=8)
        plt.title('The relationship between experience and average salary',fontsize = 12)
        plt.xlabel('Experience',fontsize=10)
        plt.ylabel('Average Salary',fontsize=10)
        plt.xticks(fontsize=7)
        plt.yticks(fontsize=7)

        """公司大小和薪资(平均值)的折线图"""
        plt.figure(6)
        plt.plot(company_mean.index, company_mean.values, linestyle='-', marker='o', color='darkorange',linewidth = 1)
        for i in range(len(company_mean.index)):
            plt.annotate(round(company_mean.values[i]), (company_mean.index[i], company_mean.values[i]), textcoords="offset points", xytext=(20,-10), ha='center')
        plt.title('The relationship between company size and average salary',fontsize = 12)
        #plt.xlabel('Company Size',fontsize=10)
        plt.ylabel('Average Salary',fontsize=10)
        plt.yticks(fontsize=7)
        plt.show()


    """词云"""
    def word_cloud(self):
        df = self.import_table_info()
        """公司福利词云"""
        plt.figure(7)
        text_benefits = ''
        for index, row in df.iterrows():
            text = row['benefits']
            text_benefits += text + ' '
        #print(text_benefits)
        font_path = "c:\WINDOWS\Fonts\MSYH.TTC" 
        img = cv2.imread('.\\analyse\\back_zoya.png',0)
        ret, mask = cv2.threshold(img, 60, 255, cv2.THRESH_BINARY_INV)
        wordcloud = WordCloud(scale = 3,mask=mask,font_path=font_path,background_color='white',min_font_size=7,colormap='viridis').generate(text_benefits)       # 创建词云对象，并生成词云图像
        plt.imshow(wordcloud, interpolation='bilinear')                     # 设置词云的样式和参数
        plt.axis('off')

        """岗位技能要求词云"""
        plt.figure(8)
        text_skills = ''
        for index, row in df.iterrows():
            text = row['skills']
            text_skills += text + ' '
        font_path = "c:\WINDOWS\Fonts\MSYH.TTC" 
        img = cv2.imread('.\\analyse\\back_cat.png',0)
        ret, mask = cv2.threshold(img, 60, 255, cv2.THRESH_BINARY_INV)
        wordcloud = WordCloud(scale = 3,mask=mask,font_path=font_path,background_color='white',min_font_size=7,colormap='Dark2').generate(text_skills)       
        plt.imshow(wordcloud, interpolation='bilinear')                    
        plt.axis('off')
        plt.show()

    

"""测试"""
"""
city = '上海'
position = 'Python'
use_case = table_extract(city,position)
average_salary,education_mean,experience_mean,company_mean = use_case.salary_print()
scatter_diagram = use_case.scatter_diagram()
line_chart = use_case.line_chart()
word_cloud = use_case.word_cloud()
"""

"""生成静态图像资源,不调用"""
def rank_cal():
    city = '上海'
    industry = {}
    Back_end_development = ['Java','c_cjiajia','PHP','Python','_net','Node_js','Golang','Hadoop','yuyinshipintuxingkaifa','数据采集','GIS工程师','全栈工程师']
    salary_1 = {}
    for item in Back_end_development:
        position = item
        use_case = table_extract(city,position)
        average_salary,education_mean,experience_mean,company_mean = use_case.salary_print()
        salary_1[item] = average_salary
    aver_1 = round(sum(list(salary_1.values()))/len(Back_end_development))
    industry['Back_end_development'] = aver_1

    Front_end_mobile = ['前端开发工程师','Android','IOS','uthreed','uefour','Cocos','技术美术']
    salary_2 = {}
    for item in Front_end_mobile:
        position = item
        use_case = table_extract(city,position)
        average_salary,education_mean,experience_mean,company_mean = use_case.salary_print()
        salary_2[item] = average_salary
    aver_2 = round(sum(list(salary_2.values()))/len(Front_end_mobile))
    industry['Front_end_mobile'] = aver_2

    Test = ['测试工程师','软件测试','自动化测试','功能测试','测试开发','硬件测试','游戏测试','性能测试','渗透测试','移动端测试']
    salary_3 = {}
    for item in Test:
        position = item
        use_case = table_extract(city,position)
        average_salary,education_mean,experience_mean,company_mean = use_case.salary_print()
        salary_3[item] = average_salary
    aver_3 = round(sum(list(salary_3.values()))/len(Test))
    industry['Test'] = aver_3

    Operations_Technology = ['运维工程师','IT技术支持','网络工程师','网络安全','系统工程师','运维开发工程师','系统管理员','DBA','系统安全','技术文档工程师']
    salary_4 = {}
    for item in Operations_Technology:
        position = item
        use_case = table_extract(city,position)
        average_salary,education_mean,experience_mean,company_mean = use_case.salary_print()
        salary_4[item] = average_salary
    aver_4 = round(sum(list(salary_4.values()))/len(Operations_Technology))
    industry['Operations_Technology'] = aver_4

    ArtificialIntelligence = ['图像算法','自然语言处理算法','大模型算法','数据挖掘','规控算法','SLAM算法','推荐算法','搜索算法','语音算法','风控算法','算法工程师','机器学习','深度学习','AI训练师']
    salary_5 = {}
    for item in ArtificialIntelligence:
        position = item
        use_case = table_extract(city,position)
        average_salary,education_mean,experience_mean,company_mean = use_case.salary_print()
        salary_5[item] = average_salary
    aver_5 = round(sum(list(salary_5.values()))/len(ArtificialIntelligence))
    industry['ArtificialIntelligence'] = aver_5

    def merge_and_sort_dictionaries(*dicts):
        merged_dict = {}
        for dictionary in dicts:
            merged_dict.update(dictionary)
        sorted_dict = dict(sorted(merged_dict.items(), key=lambda item: item[1], reverse=True))
        return sorted_dict
    ocupation_rank = merge_and_sort_dictionaries(salary_1,salary_2,salary_3,salary_4,salary_5)

    return industry,ocupation_rank

industry, occupation_rank = rank_cal()
def chart1():
    keys1 = ['后端开发','前端/移动开发','测试','运维/技术支持','AI']
    values1 = list(industry.values())
    plt.figure(figsize=(6, 4))
    plt.bar(keys1, values1, color = 'bisque')
    plt.xlabel('模块名称')
    plt.title('平均月薪')
    plt.xticks(rotation=0)
    for i, v in enumerate(values1):
        plt.text(i, v, str(v), ha='center', va='bottom')
    save_directory = os.path.join(os.getcwd(), 'Visualization', 'static')
    save_path = os.path.join(save_directory, 'bar_chart1.png')
    if os.path.exists(save_path):
        os.remove(save_path)
    plt.savefig(save_path, bbox_inches='tight')

def chart2():
    keys2 = list(occupation_rank.keys())[:10]
    for i in range(len(keys2)):
        if 'y' in keys2[i]:
            keys2[i] = '语音/视频/图形开发'
    values2 = list(occupation_rank.values())[:10]
    plt.figure(figsize=(6, 4))
    bars = plt.barh(keys2, values2,color = 'bisque')  # 使用plt.barh()绘制横向柱状图
    plt.gca().invert_yaxis()  # 反转 y 轴顺序
    plt.xlabel('平均月薪')
    plt.title('高薪职业前十名')
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height() / 2, str(int(width)), ha='left', va='center')
    save_directory = os.path.join(os.getcwd(), 'Visualization', 'static')
    save_path = os.path.join(save_directory, 'bar_chart2.png')
    if os.path.exists(save_path):
        os.remove(save_path)
    plt.savefig(save_path, bbox_inches='tight')

chart1()
chart2()
