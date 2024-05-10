from flask import Flask, request, render_template, jsonify, Response
from flask import redirect
from flask import url_for
from flask import request
import sys
import os
import json
import numpy as np
from model.check_login import *
from model.check_register import *
import re
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Analyse.DataAnalyse import table_extract

app = Flask(__name__)

templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app.template_folder = templates_dir     # 设定相对路径,导入.html文件

@app.route('/')
def initialpage():
    return redirect(url_for('user_login'))

@app.route('/login',methods=['GET','POST'])
def user_login():
    if request.method=='POST':                  # 注册发送的请求为POST请求
        username = request.form['username']
        password = request.form['password']
        if is_null(username,password):
            login_massage = "温馨提示: 请输入账号和密码"
            return render_template('login.html', message=login_massage)
        elif is_existed(username, password):
            return redirect(url_for('home'))
        elif exist_user(username):
            login_massage = "温馨提示: 密码错误,请重新输入正确密码"
            return render_template('login.html', message=login_massage)
        else:
            login_massage = "温馨提示: 该用户不存在,请先注册"
            return render_template('login.html', message=login_massage)
    return render_template('login.html')

@app.route("/regiser",methods=["GET", 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if is_null(username,password):
            login_massage = "温馨提示: 请输入账号和密码"
            return render_template('register.html', message=login_massage)
        elif exist_user(username):
            login_massage = "温馨提示: 用户已存在，请直接登录"
            return redirect(url_for('login'))
        else:
            add_user(request.form['username'], request.form['password'] )
            return redirect(url_for('home'))
    return render_template('register.html')


@app.route('/home',methods=['GET', 'POST'])
def home():
    return render_template('index.html')

    
@app.route('/home/show_info', methods=['POST'])
def show_info():
    if request.method == 'POST':
        data = request.get_json()
        city = data['city']
        position = data['position']
        use_case = table_extract(city, position)
        df = use_case.import_table_info()
        result = df.to_dict(orient='records')
        return jsonify(result=result)
    else:
        return "Invalid request method."

@app.route('/home/scatter_plot_education', methods=['POST'])
def scatter_plot_education():
    if request.method == 'POST':
        data = request.get_json()
        city = data['city']
        position = data['position']
        use_case = table_extract(city, position)
        df = use_case.import_table_info()
        df['salary_pro'] = df['salary'].apply(use_case.salary_process)
        unique_education = df['education'].unique()
        label_indices = np.arange(len(unique_education))
        label_index_mapping = dict(zip(unique_education, label_indices))
        indices = df['education'].map(label_index_mapping)
        data = []
        for salary_pro, index in zip(df['salary_pro'], indices):
            data.append([salary_pro, index])
        option = {
            'title': {
                'text': 'Scatter diagram between salary and education',
                'left': 'center',
                'top': 20,
                'textStyle': {
                    'fontSize': 24
                }
            },
            'tooltip': {},
            'xAxis': {
                'type': 'value',
                'name': 'Salary',
                'nameLocation': 'middle',
                'nameGap': 30,
                'nameTextStyle': {
                    'fontSize': 20
                },
                'axisLabel': {
                    'fontSize': 12
                },
                "axisLine": {  
                    "show": True,  
                    "lineStyle": {
                        "color": "#333",  
                        "width": 1  
                    }
                }
            },
            'yAxis': {
                'type': 'category',
                'nameLocation': 'middle',
                'nameGap': 40,
                'data': unique_education,
                'axisLabel': {
                    'fontSize': 12
                },
                "axisLine": {  
                    "show": True,  
                    "lineStyle": {
                        "color": "#333",  
                        "width": 1  
                    }
                }
            },
            'series': [{
                'type': 'scatter',
                'data': data,
                'symbolSize': 4,
                'label': {
                    'show': False
                },
                'itemStyle': {
                }
            }]
        }
        option_copy = option.copy()  
        option_copy['yAxis']['data'] = option_copy['yAxis']['data'].tolist()  # 转换 ndarray 为列表
        echarts_code = json.dumps(option_copy)
        return echarts_code
    else:
        return "Invalid request method."

@app.route('/home/scatter_plot_experience', methods=['POST'])
def scatter_plot_experience():
    if request.method == 'POST':
        data = request.get_json()
        city = data['city']
        position = data['position']
        use_case = table_extract(city, position)
        df = use_case.import_table_info()
        df['salary_pro'] = df['salary'].apply(use_case.salary_process)
        unique_experience = df['experience'].unique()
        label_indices = np.arange(len(unique_experience))
        label_index_mapping = dict(zip(unique_experience, label_indices))
        indices = df['experience'].map(label_index_mapping)
        data = []
        for salary_pro, index in zip(df['salary_pro'], indices):
            data.append([salary_pro, index])
        option = {
            'title': {
                'text': 'Scatter diagram between salary and experience',
                'left': 'center',
                'top': 20,
                'textStyle': {
                    'fontSize': 24
                }
            },
            'tooltip': {},
            'xAxis': {
                'type': 'value',
                'name': 'Salary',
                'nameLocation': 'middle',
                'nameGap': 30,
                'nameTextStyle': {
                    'fontSize': 20
                },
                'axisLabel': {
                    'fontSize': 12
                },
                "axisLine": {  
                    "show": True,  
                    "lineStyle": {
                        "color": "#333",  
                        "width": 1  
                    }
                }
            },
            'yAxis': {
                'type': 'category',
                'nameLocation': 'middle',
                'nameGap': 40,
                'data': unique_experience,
                'axisLabel': {
                    'fontSize': 12
                },
                "axisLine": {  
                    "show": True,  
                    "lineStyle": {
                        "color": "#333",  
                        "width": 1  
                    }
                }
            },
            'series': [{
                'type': 'scatter',
                'data': data,
                'symbolSize': 4,
                'label': {
                    'show': False
                },
                'itemStyle': {
                }
            }]
        }
        option_copy = option.copy()  
        option_copy['yAxis']['data'] = option_copy['yAxis']['data'].tolist()  # 转换 ndarray 为列表
        echarts_code = json.dumps(option_copy)
        return echarts_code
    else:
        return "Invalid request method."
    
@app.route('/home/scatter_plot_company_size', methods=['POST'])
def scatter_plot_company_size():
    if request.method == 'POST':
        data = request.get_json()
        city = data['city']
        position = data['position']
        use_case = table_extract(city, position)
        df = use_case.import_table_info()
        df['salary_pro'] = df['salary'].apply(use_case.salary_process)
        unique_company_size = df['company_size'].unique()
        label_indices = np.arange(len(unique_company_size))
        label_index_mapping = dict(zip(unique_company_size, label_indices))
        indices = df['company_size'].map(label_index_mapping)
        data = []
        for salary_pro, index in zip(df['salary_pro'], indices):
            data.append([salary_pro, index])
        option = {
            'title': {
                'text': 'Scatter diagram between salary and company size',
                'left': 'center',
                'top': 20,
                'textStyle': {
                    'fontSize': 24
                }
            },
            'tooltip': {},
            'xAxis': {
                'type': 'value',
                'name': 'Salary',
                'nameLocation': 'middle',
                'nameGap': 30,
                'nameTextStyle': {
                    'fontSize': 20
                },
                'axisLabel': {
                    'fontSize': 12
                },
                "axisLine": {  
                    "show": True,  
                    "lineStyle": {
                        "color": "#333",  
                        "width": 1  
                    }
                }
            },
            'yAxis': {
                'type': 'category',
                'nameLocation': 'middle',
                'nameGap': 40,
                'data': unique_company_size,
                'axisLabel': {
                    'fontSize': 12
                },
                "axisLine": {  
                    "show": True,  
                    "lineStyle": {
                        "color": "#333",  
                        "width": 1  
                    }
                }
            },
            'series': [{
                'type': 'scatter',
                'data': data,
                'symbolSize': 4,
                'label': {
                    'show': False
                },
                'itemStyle': {
                }
            }]
        }
        option_copy = option.copy()  
        option_copy['yAxis']['data'] = option_copy['yAxis']['data'].tolist()  # 转换 ndarray 为列表
        echarts_code = json.dumps(option_copy)
        return echarts_code
    else:
        return "Invalid request method."

@app.route('/home/education_chart', methods=['POST'])
def education_chart():
    if request.method == 'POST':
        data = request.get_json()
        city = data['city']
        position = data['position']
        use_case = table_extract(city, position)
        average_salary, education_mean, experience_mean, company_mean = use_case.salary_print()
        # 构造echarts所需的数据格式
        data = []
        for i, value in enumerate(education_mean.values):
            data.append([value, education_mean.index[i]])
        # 构建echarts所需的option对象
        option = {
            "title": {
                "text": "The relationship between education and average salary",
                "left": "center",
                "top": 20,
                "textStyle": {
                    "fontSize": 24
                }
            },
            "tooltip": {},
            "xAxis": {
                "type": "value",
                "name": "Average Salary",
                "nameLocation": "middle",
                "nameGap": 30,
                "nameTextStyle": {
                    "fontSize": 20
                },
                "axisLabel": {
                    "fontSize": 16
                },
                "axisLine": {  
                    "show": True,  
                    "lineStyle": {
                        "color": "#333",  
                        "width": 1  
                    }
                }
            },
            "yAxis": {
                "type": "category",
                "nameLocation": "middle",
                "nameGap": 40,
                "data": education_mean.index.tolist(),
                "axisLabel": {
                    "fontSize": 16
                },
                "axisLine": {  
                    "show": True,  
                    "lineStyle": {
                        "color": "#333",  
                        "width": 1  
                    }
                }
            },
            "series": [{
                "type": "bar",
                "data": data,
                "barWidth": 40,
                "itemStyle": {
                    "color": "khaki"
                },
                "label": {
                    "show": True,
                    "position": "insideRight",
                    "color": "black",
                    "fontSize": 14
                }
            }]
        }
        # 将option转换为JSON字符串返回给前端
        return json.dumps(option)
    else:
        return "Invalid request method."

@app.route('/home/experience_chart', methods=['POST'])
def experience_chart():
    if request.method == 'POST':
        data = request.get_json()
        city = data['city']
        position = data['position']
        use_case = table_extract(city, position)
        average_salary, education_mean, experience_mean, company_mean = use_case.salary_print()
        data = []
        for i, value in enumerate(experience_mean.values):
            data.append([experience_mean.index[i], value])
        
        # 构建echarts所需的option对象
        option = {
            "title": {
                "text": "The relationship between experience and average salary",
                "left": "center",
                "top": 20,
                "textStyle": {
                    "fontSize": 24
                }
            },
            "tooltip": {},
            "xAxis": {
                "type": "category",
                "name": "Experience",
                "nameLocation": "middle",
                "nameGap": 30,
                "nameTextStyle": {
                    "fontSize": 20
                },
                "axisLabel": {
                    "fontSize": 16
                },
                "axisLine": {  
                    "show": True,  
                    "lineStyle": {
                        "color": "#333",  
                        "width": 1  
                    }
                },
                "data": experience_mean.index.tolist()
            },
            "yAxis": {
                "type": "value",
                "nameLocation": "middle",
                "nameGap": 40,
                "axisLabel": {
                    "fontSize": 16
                },
                "axisLine": {  
                    "show": True,  
                    "lineStyle": {
                        "color": "#333",  
                        "width": 1  
                    }
                }
            },
            "series": [{
                "type": "bar",
                "data": data,
                "barWidth": 50,
                "itemStyle": {
                    "color": "cornflowerblue"
                },
                "label": {
                    "show": True,
                    "position": "top",
                    "fontSize": 16
                }
            }]
        }
        # 将option转换为JSON字符串返回给前端
        return json.dumps(option)
    else:
        return "Invalid request method."

@app.route('/home/company_size_chart', methods=['POST'])
def company_size_chart():
    if request.method == 'POST':
        data = request.get_json()
        city = data['city']
        position = data['position']
        use_case = table_extract(city, position)
        average_salary, education_mean, experience_mean, company_mean = use_case.salary_print()
        data = []
        for i, value in enumerate(company_mean.values):
            data.append([company_mean.index[i], value])
        option = {
            "title": {
                "text": "The relationship between company size and average salary",
                "left": "center",
                "top": 20,
                "textStyle": {
                    "fontSize": 24
                }
            },
            "tooltip": {},
            "xAxis": {
                "type": "category",
                "name": "Company Size",
                "nameLocation": "middle",
                "nameGap": 30,
                "nameTextStyle": {
                    "fontSize": 20
                },
                "axisLabel": {
                    "fontSize": 16
                },
                "axisLine": {  
                    "show": True,  
                    "lineStyle": {
                        "color": "#333",  
                        "width": 1  
                    }
                },
                "data": company_mean.index.tolist()
            },
            "yAxis": {
                "type": "value",
                "nameLocation": "middle",
                "nameGap": 40,
                "axisLabel": {
                    "fontSize": 16
                },
                "axisLine": {  
                    "show": True,  
                    "lineStyle": {
                        "color": "#333",  
                        "width": 1  
                    }
                },
            },
            "series": [{
                "type": "line",
                "data": data,
                "lineStyle": {
                    "color": "darkorange",
                    "width": 2
                },
                "itemStyle": {
                    "color": "darkorange"
                },
                "symbol": "circle",
                "symbolSize": 6,
                "label": {
                    "show": True,
                    "position": "top",
                    "fontSize": 14
                }
            }]
        }
        return json.dumps(option)
    else:
        return "Invalid request method."

@app.route('/home/benefits_cloud', methods = ['POST'])
def benefits_cloud():
    if request.method == 'POST':
        data = request.get_json()
        city = data['city']
        position = data['position']
        use_case = table_extract(city, position)
        df = use_case.import_table_info()
        text_benefits = ''
        word_count = {}  # 创建空字典用于存储词语出现的次数
        # 将一列中的所有文本合并在一起
        for index, row in df.iterrows():
            text = row['benefits']
            text_benefits += text + ' '
        texts = re.split(r'[，\s]', text_benefits)
        for text in texts:
            if text:
                words = text.split(" ")             # 将文本按空格分割成词语列表
                for word in words:
                    if word in word_count:
                        word_count[word] += 1       # 如果词语已存在于字典中，增加词频
                    else:
                        word_count[word] = 1        # 如果词语不存在于字典中，添加新的词语并设置词频为1
        word_count = {k: v for k, v in word_count.items() if v > 1}
        wordcloud_data = {
            "word_count": word_count,               
        }
        return json.dumps(wordcloud_data)
    else:
        return "Invalid request method."
    
@app.route('/home/skills_cloud', methods = ['POST'])
def skills_cloud():
    if request.method == 'POST':
        data = request.get_json()
        city = data['city']
        position = data['position']
        use_case = table_extract(city, position)
        df = use_case.import_table_info()
        text_skills = ''
        word_count = {}  # 创建空字典用于存储词语出现的次数
        # 将一列中的所有文本合并在一起
        for index, row in df.iterrows():
            text = row['skills']
            text_skills += text + ' '
        texts = re.split(r'[,\s]', text_skills)
        for text in texts:
            if text:
                words = text.split(" ")  # 将文本按空格分割成词语列表
                for word in words:
                    if word in word_count:
                        word_count[word] += 1  # 如果词语已存在于字典中，增加词频
                    else:
                        word_count[word] = 1  # 如果词语不存在于字典中，添加新的词语并设置词频为1
        word_count = {k: v for k, v in word_count.items() if v > 1}
        wordcloud_data = {
            "word_count": word_count,   # 将词频字典添加到返回的数据中
        }
        return json.dumps(wordcloud_data)
    else:
        return "Invalid request method."
  
@app.route('/home/rank', methods = ['GET','POST'])
def rank():
    if request.method == 'POST':
        return render_template('rank.html')
    elif request.method == 'GET':
        return render_template('rank.html')
    else:
        return "Invalid request method."

if __name__=="__main__":
    app.run()
    
    



