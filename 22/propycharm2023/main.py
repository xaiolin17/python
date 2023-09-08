import math
import random
import time
from bs4 import BeautifulSoup
from datetime import datetime
from fake_useragent import UserAgent
import requests
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# + '#!tab=history'
url = 'https://www.mql5.com/zh/signals/1636506?source=Site+Main'
# url ='https://www.mql5.com/zh/signals/1636506?source=Site+Main#!tab=history'
# headers = {
#         'user-agent': UserAgent().random,
#     }

# user_data_dir = r'C:\Users\01\AppData\Local\Google\Chrome\User Data'
# response = requests.get('url', verify=True, headers=headers)
# 调用环境变量指定的PhantomJS浏览器创建浏览器对象
# user_option  = webdriver.ChromeOptions()
# user_option .add_argument(f'--user-data-dir={user_data_dir}')
# # get方法会一直等到页面被完全加载，然后才会继续程序, 跳转到指定的URL

# driver = webdriver.Chrome(options=user_option)
# driver.get(url)

# options = ChromeOptions()
# options.add_experimental_option("debuggerAddress", "127.0.0.1:9014")
# browser = webdriver.Chrome(executable_path=r"C:\Program Files\Google\Chrome\Application\chromedriver.exe",
#                            chrome_options=options)


# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# driver = webdriver.Chrome()
'''username = 'xiaolin17'
password = 'CdDEFAcw'
driver = webdriver.Chrome()
driver.get(url)

#点击登录
login_btn = driver.find_element(By.XPATH, '//i[text()="登录"]')
login_btn.click()'''
USERNAME = 'xiaolin17'
PASSWORD = 'CdDEFAcw'

options = Options()
driver = webdriver.Chrome(options=options)
# browser=webdriver.PhantomJS()    # 不跳出界面浏览器驱动，在后台运行浏览器
driver.get(url+'#!tab=history')
#点击登录
login_btn = driver.find_element(By.XPATH, '//a[text()="登录"]')
login_btn.click()
#输入账号密码
input_username = driver.find_element(By.XPATH, '//input[@id="Login"]')
input_username.send_keys(USERNAME)

input_password = driver.find_element(By.XPATH, '//input[@id="Password"]')
input_password.send_keys(PASSWORD)

#提交登录
submit_btn = driver.find_element(By.XPATH, '//input[@id="loginSubmit"]')
submit_btn.click()

time.sleep(3)
#点击交易历史记录
history_btn = driver.find_element(By.ID, 'tab_history')
history_btn.click()

# print(len(souptbody)) len=1
result = []
#拿到页码方便后序翻页
len_page = int(driver.find_element("class name", "paginatorEx").text[-1])

for page in range(1,len_page+1):
    #点击翻页
    page_btn = driver.find_element(By.XPATH, '//a[text()=' + str(page) + ']')
    page_btn.click()
    time.sleep(1)
    # 包含数据的div ID
    data = driver.find_element("id", "signal_tab_content_positions")
    # 拿到tbody表格html
    soupdiv = BeautifulSoup(data.get_attribute('outerHTML'), 'lxml')
    souptbody = soupdiv.find_all(name='tbody')
    #获取每一行
    for tr in souptbody[0].find_all(name='tr'):
        tdlist = tr.find_all(name='td')
        print(tdlist[-1])
        print('-------------------------------------')
        print(tdlist[0])
        print("####################################")

        #获取每一格
        dict = {}
        for i in range(len(tdlist)):
            tdlist_copy = tdlist.copy()
            if i == 0:
                dict['时间1'] = tdlist[i].text
            elif i == 1:
                dict['类型'] = tdlist[i].text
            elif i == 2:
                dict['交易量'] = tdlist[i].text
            elif i == 3:
                dict['交易品种'] = tdlist[i].text
            elif i == 4:
                dict['价格1'] = tdlist[i].text
            elif i == 5:
                dict['时间2'] = tdlist[i].text
            elif i == 6:
                dict['价格2'] = tdlist[i].text
            elif i == 7:
                dict['佣金'] = tdlist[i].text
            elif i == 8:
                dict['库存费'] = tdlist[i].text
            elif i == 9:
                dict['利润'] = tdlist[i].text
        #每一行数据放到一个位置
        result.append(dict)

print(result)
print(len(result))
# print(data.get_attribute('outerHTML'))


# soup = BeautifulSoup(html, "html.parser")
"""ele_keys = [
"id", # 对象的ID
"tag_name", # 元素的标签
"location", # 在页面中的位置（x,y）坐标
"size", # 元素大小
"rect", # 位置 + 大小
"parent", # WebDriver 对象
]
for key in ele_keys:
    print(key)
    print(getattr(data, key))
    print("-" * 20)"""


#data = driver.find_element(By.ID, 'signal_tab_content_positions')
#histo ry_pag = BeautifulSoup(data, "html.parser")

""""""
# data = data.find_elements(By.XPATH, '//tr[]')
# for i in data:
#     print(i.text)

# for i in data.text.split():
#     print(i)

# print(history_pag)
#######################################

#newsList = soup.find_all('div', id='tab_content_history',class_="tab__content selected")
#print(newsList)

# for i in range(5):
#     shoplist = driver.find_elements(By.CSS_SELECTOR, ".shoplist li")
#     for li in shoplist:
#         print(li.find_element(By.CSS_SELECTOR, "a").get_attribute("title"))
#     # 获取下一页按钮
#     next = driver.find_element(By.LINK_TEXT, "下一页")
#     next.click()

# response = requests.get(url, verify=True, headers=headers)
# print(response.text)

driver.quit()
