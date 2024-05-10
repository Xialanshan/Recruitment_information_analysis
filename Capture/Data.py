from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
import random
import time
import re
import mysql.connector
import city_position_details as cp_details
from pypinyin import lazy_pinyin
from selenium.webdriver.support.ui import WebDriverWait
"""
输入: 城市名称和职业名称(后续可视化以点击选择操作代替)
查找: 运行CityPosition.py文件后,查找用户目标城市和职业,返回两个代号,传入Craw类
输出: 目标城市目标职业的所有招聘条目,存储在result中对应的.xlsx文件中
"""

"""连接数据库"""
from environs import Env    # new
env = Env()     # new
env.read_env()

db = mysql.connector.connect(
    host=env('HOST'),
    user=env('USER'),
    password=env('PASSWORD'),
    database=env('DATABASE')
)

"""产生随机的user-agent"""
def get_ua():
    first_num = random.randint(55, 76)
    third_num = random.randint(0, 3800)
    fourth_num = random.randint(0, 140)
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_14_5)'
    ]
    Edge_version = 'Edge/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                   '(KHTML, like Gecko)', Edge_version, 'Safari/537.36']
                  )
    return ua


"""抓取特定城市特定职位的所有招聘条目"""
class Craw():
    """初始化城市和岗位"""
    def __init__(self, city: str, position: str):
        self.city = city
        self.position = position

    """selenium操作准备"""
    def selenium_initial(self):
        edge_options = Options()
        User_Agent = get_ua()
        edge_options.add_argument('--disable-gpu')
        edge_options.add_argument(f"--user-agent={User_Agent}")
        edge_options.add_experimental_option('detach', True)
        driver = webdriver.Edge("C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe",
                                options=edge_options)
        return driver


    """获取当前情况下总的页面数"""
    def get_number(self):
        driver = self.selenium_initial()
        url = 'https://www.zhipin.com/web/user/?ka=header-login'
        driver.get(url)
        driver.implicitly_wait(10)
        element = driver.find_element(By.CLASS_NAME,'switch-tip')
        element.click()
        wait = WebDriverWait(driver, 5)
        endnumber = 0
        url = f'https://www.zhipin.com/web/geek/job?query=&city={self.city}&position={self.position}&page=1'
        driver.get(url)
        driver.implicitly_wait(10)
        try:
            html_content = driver.page_source  # 获取完整渲染后的页面内容
            soup = BeautifulSoup(html_content, "html.parser")
            elements = soup.find("div", class_="pagination-area").find("div", class_="pager text-center").find(
                "div", class_="options-pages").find_all("a", class_="")
            for element in elements:
                text = element.get_text()
                if text.isdigit():
                    number = int(text)
                    if number > endnumber:
                        endnumber = number
        except Exception as e:
            print(f"获取页面数异常: {e}")
        finally:
            driver.quit()
        return endnumber

    """抓取所有相关网页"""
    def craw_all_htmls(self):
        data = []
        endnumber = self.get_number()
        for idx in range(1, endnumber + 1):
            driver = self.selenium_initial()
            try:
                driver.get(
                    f'https://www.zhipin.com/web/geek/job?query=&city={self.city}&position={self.position}&page={idx}')
                driver.implicitly_wait(10)
                html_content = driver.page_source
                soup = BeautifulSoup(html_content, "html.parser")
                article_items = (soup.find_all("li", class_="job-card-wrapper"))

                """原始信息采集区"""
                for article_item in article_items:
                    info1 = article_item.find("div", class_="job-card-body clearfix")
                    info2 = article_item.find("div", class_="job-card-footer clearfix")
                    job_name = info1.find("div", class_="job-title clearfix").find("span", class_="job-name").get_text()
                    job_area = info1.find("div", class_="job-title clearfix").find("span",
                                                                                     class_="job-area-wrapper").find(
                        "span", class_="job-area").get_text()
                    salary = info1.find("div", class_="job-info clearfix").find("span", class_="salary").get_text()
                    requirement_list = info1.find("div", class_="job-info clearfix").find("ul",
                                                                                           class_="tag-list").find_all(
                        "li")
                    require_list = [requirement.get_text() for requirement in requirement_list]
                    company_name = info1.find("div", class_="job-card-right").find("div", class_="company-info").find(
                        "h3", class_="company-name").find('a').get_text()
                    tag_list = info2.find("ul", class_="tag-list").find_all("li")
                    workfare = info2.find('div', 'info-desc').get_text()
                    scale_of_company = info1.find("div", class_="job-card-right").find("div",
                                                                                        class_="company-info").find(
                        'ul', class_='company-tag-list').find_all('li')
                    scale_of_company = scale_of_company[-1].get_text()
                    skills_list = []  # 岗位方向
                    result = [re.sub(r'^\s*::before\s*', '', item.get_text().strip()) for item in tag_list]
                    for res in result:
                        res = res.replace('"', '')
                        skills_list.append(res)
                    skills_string = ', '.join(skills_list)
                    data.append({
                        "job-name": job_name,
                        "job-area": job_area,
                        "salary": salary,
                        "experience_requirement": require_list[0],
                        "education_requirement": require_list[1],
                        'workfare': workfare,
                        "skills": skills_string,
                        "company": company_name,
                        "scale of company": scale_of_company
                    })
                print(f"爬取第{idx}页成功")
            except Exception as e:
                print(f"爬取第{idx}页异常: {e}")
            finally:
                driver.quit()
        return data


"""数据库bosszhipin表的命名"""
def name(city: str, position: str):
    """
    city和position传入的是中文字符串,而不是编号
    """
    city_pinyin = lazy_pinyin(city)
    city_name = ''.join(city_pinyin)
    position_pinyin = lazy_pinyin(position)
    position_name = ''.join(position_pinyin)
    return city_name, position_name


"""判断表是否存在"""
def is_table_exists(city: str, position: str):
    city_name, position_name = name(city, position)
    cursor = db.cursor()
    cursor.execute("SHOW TABLES LIKE %s", (f'{city_name}_{position_name}',))
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False


"""将df类型的数据存储进数据库"""
def df_to_sql(df):
    city_name, position_name = name(city, position)
    cursor = db.cursor()
    drop_table_query = f"DROP TABLE IF EXISTS {city_name}_{position_name}"  # 如果表已经存在,就删除
    cursor.execute(drop_table_query)
    create_table_query = f'''
    CREATE TABLE IF NOT EXISTS {city_name}_{position_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        location VARCHAR(255),
        salary VARCHAR(255),
        experience VARCHAR(255),
        education VARCHAR(255),
        benefits VARCHAR(255),
        skills VARCHAR(255),
        company VARCHAR(255),
        company_size VARCHAR(255)
    )'''
    cursor.execute(create_table_query)

    try:
        insert_query = f'''
        INSERT INTO {city_name}_{position_name} (title, location, salary, experience, education, benefits, skills, company, company_size)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        data_tuples = [tuple(row) for row in df.values.tolist()]
        cursor.executemany(insert_query, data_tuples)  # 执行插入操作
        db.commit()
        print(f'{city}_{position}信息存储完毕')
    except Exception as e:
        db.rollback()
        print(f'存储数据异常: {e}')

    cursor.close()


for city in cp_details.data_city.keys():
    city_number = cp_details.data_city[city]
    for position in cp_details.data_position:
        position_number = cp_details.data_position[position]
        """数据爬取实例"""
        if is_table_exists(city, position):
            continue
        else:
            Craw_bosszhipin = Craw(city_number, position_number)  # 建立Craw类实例
            data = Craw_bosszhipin.craw_all_htmls()  # 调用craw_all_htmls方法选择出指定的信息
            df = pd.DataFrame(data)
            df = df.fillna('')  # 将所有空值替换为空字符串
            result = df_to_sql(df)
            time.sleep(10)

db.close()
