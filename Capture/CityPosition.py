from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import re


"""
输入: 无(在后续.py文件中直接运行)
输出: 已开通城市的代号和Boss直聘所有既定职业的代号
        data_city(dict)     data_postion_discrete(dict)
"""


"""产生随机的user-agent"""
def get_ua():           
    first_num  = random.randint(55,76)
    third_num = random.randint(0, 3800)
    fourth_num = random.randint(0, 140)
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_14_5)']
    edge_version = 'Edge/{}.0.{}.{}'.format(first_num, third_num, fourth_num)
    ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                   '(KHTML, like Gecko)', edge_version, 'Safari/537.36']
                  )
    return ua


""" selenium操作准备"""
def selenium_initial():        
    edge_options = Options()
    User_Agent = get_ua()
    edge_options.add_argument('--headless')                     # 无头模式
    edge_options.add_argument('--disable-gpu')                  # 禁用GPU
    edge_options.add_argument(f"--user-agent={User_Agent}")     # 随机user-agent
    edge_options.add_experimental_option('detach', True)        # 网页后续关闭
    driver = webdriver.Edge("C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe", options = edge_options)
    return driver


"""以上海为初始城市抓取所有的城市代号和既定的职业编号"""
def initial_mark():             
    driver = selenium_initial()     
    driver.get('https://www.zhipin.com/shanghai/?ka=city-sites-101020100')
    time.sleep(3)

    data_city = {}       # 字典存储城市和代号的键值对
    """寻找城市代号"""
    element = driver.find_element(By.CSS_SELECTOR, 'div.nav-city > p.nav-city-box > span.nav-city-selected')
    element.click()
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'dialog-container')))  # 在弹出小框的页面的内容上继续操作

    element_city_default = driver.find_element(By.CLASS_NAME, 'city-name').find_element(By.TAG_NAME,'a')
    data_city[element_city_default.text] = re.search(r'\b\d{9}\b', element_city_default.get_attribute('ka')).group()
    element_city_others = driver.find_elements(By.CLASS_NAME, 'city-item')
    for element_city in element_city_others:
        element_city = element_city.find_element(By.TAG_NAME, 'a')
        data_city[element_city.text] = re.search(r'\b\d{9}\b', element_city.get_attribute('ka')).group()

    element_close = driver.find_element(By.CLASS_NAME, 'icon-close')
    driver.execute_script('arguments[0].click()',element_close)         # 模拟javascript点击,解决弹窗阻挡问题

    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'job-menu-wrapper')))     # 切换到主页,爬取职位信息

    data_position_discrete = {}      # 字典每个职业的代号
    data_position_concentrate = {}  # 三层字典存储大类型小类型每个职业的代号

    """寻找职业代号"""
    menu_subs = driver.find_elements(By.CLASS_NAME,'menu-sub')
    for menu_sub in menu_subs:
        large_class_name = menu_sub.find_element(By.TAG_NAME,'p').get_attribute('innerHTML')
        little_classes = menu_sub.find_elements(By.TAG_NAME,'li')
        lc = {}
        for little_class in little_classes:
            little_class_name = little_class.find_element(By.TAG_NAME,'h4').get_attribute('innerHTML')
            little_class_details = little_class.find_elements(By.TAG_NAME,'a')
            lc_details = {}
            for little_class_detail in little_class_details:
                data_position_discrete[little_class_detail.get_attribute('innerHTML')] = re.search(r'\d+', little_class_detail.get_attribute('ka')).group()
                lc_details[little_class_detail.get_attribute('innerHTML')] = re.search(r'\d+', little_class_detail.get_attribute('ka')).group()
            lc[little_class_name] = lc_details
        data_position_concentrate[large_class_name] = lc
    driver.quit()
    return data_city, data_position_discrete, data_position_concentrate

data_city, data_position_discrete, data_position_concentrate = initial_mark()
