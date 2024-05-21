#可以正常爬取tk数据

import psutil
import os
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from openpyxl import Workbook
import random


def close_all_excel():
    for process in psutil.process_iter():
        try:
            # 检查每个进程的名称
            process_name = process.name()
            if process_name == "EXCEL.EXE":
                process.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

close_all_excel()


def get_new_filename(base_name="1.xlsx"):
    counter = 1
    while os.path.exists(base_name):
        counter += 1
        base_name = f"{counter}.xlsx"
    return base_name

# 检查 Chrome 是否已安装
chrome_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
if not os.path.exists(chrome_path):
    print('启动程序错误，没有正确安装Chrome浏览器')
    exit(0)

# 设置Chrome调试模式的数据存放路径（您的Google Chrome的用户数据目录）
data_dir = r'C:\Users\shenlizhen\AppData\Local\Google\Chrome\User Data\Profile 2'

# 通过子进程模式启动Chrome浏览器
subprocess.Popen(f'"{chrome_path}" --remote-debugging-port=9527 --user-data-dir="{data_dir}"')

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")

# 指定 chromedriver 的路径
chromedriver_path = "D:\chromedriver-win64\chromedriver.exe"
s = Service(chromedriver_path)

# 尝试启动浏览器
try:
    browser = webdriver.Chrome(service=s, options=options)
except Exception as e:
    print(f"启动浏览器出错：{e}")
    exit(0)

# 这是您提供的关键词列表
keywords = [
    "tiktoktips",
"becomeaninfluencer",
"smallbusinesstips",
]

base_search_url = "https://www.tiktok.com/search?q="

desired_handles = 70
# 这是您提供的关键词列表
total_links = []  # 用于存储所有关键词中提取的链接
for keyword in keywords:
    search_url = base_search_url + keyword
    browser.get(search_url)
    time.sleep(8)

    current_keyword_links = set()  # 为当前关键词创建一个新的集合
    no_new_links_count = 0
    prev_link_count = 0

    while len(current_keyword_links) < desired_handles:
        # 获取标题文本
        user_handles = []
        for i in range(desired_handles):
            try:
                title_xpath = f'//*[@id="search_top-item-user-link-{i}"]/div/p'
                title_element = browser.find_element(By.XPATH, title_xpath)
                user_handles.append(title_element.text)
            except:
                break

        # 构造完整链接并添加到集合
        base_url = "https://www.tiktok.com/@"
        for handle in user_handles:
            full_url = base_url + handle
            current_keyword_links.add(full_url)

        # 检查链接的数量是否有增加
        if len(current_keyword_links) == prev_link_count:
            no_new_links_count += 1
        else:
            no_new_links_count = 0

        prev_link_count = len(current_keyword_links)

        # 如果连续5次滚动后链接的数量没有增加，退出循环
        if no_new_links_count >= 5:
            break

        # 滚动页面并等待3秒
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # 如果已经累计到达了50条数据，则退出滚动循环
        if len(current_keyword_links) >= desired_handles:
            break

    # 打印当前关键词收集的链接
    print(f"Collected links for keyword '{keyword}':")
    for link in current_keyword_links:
        print(link)
    total_links.extend(list(current_keyword_links))

# 用于获取数据的部分
# 创建一个新的工作簿
wb = Workbook()
ws = wb.active

for link in total_links:
    browser.get(link)
    time.sleep(random.uniform(2, 5))  # 等待页面加载
    # ... [其他代码]





    # 抓取信息并保存到Excel
    try:
        fl_element = browser.find_element(By.XPATH, '//*[@id="main-content-others_homepage"]/div/div[1]/h3/div[2]/strong')
        flw = fl_element.text
        print(flw)

        # 尝试点击第一个元素
        click_element = browser.find_element(By.XPATH,
                                             '//*[@id="main-content-others_homepage"]/div/div[2]/div[2]/div/div[1]/div[1]/div/div/a/div/div[2]/strong')
    except:
        # 如果第一个元素不可用，尝试点击第二个元素
        try:
            click_element = browser.find_element(By.XPATH,
                                                 '//*[@id="main-content-others_homepage"]/div/div[2]/div[3]/div/div[1]/div[1]/div/div/a/div/div[2]/strong')
        except Exception as e:
            print(f"Error while trying to click: {e}")
            continue

    click_element.click()
    time.sleep(5)

    # 点击后尝试获取元素的文本内容
    try:
        data_element = browser.find_element(By.XPATH,
                                            '//*[@id="app"]/div[2]/div[4]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/a[2]/span[2]/span[3]')
        datas = data_element.text
        print(datas)
        ws.append([flw, link, datas])
    except Exception as e:
        print(f"Error while getting data: {e}")
        print(f"Error occurred at link: {link}")

    except Exception as e:
        print(f"Error while getting data after click: {e}")






new_filename = get_new_filename()
wb.save(new_filename)
print(f"{new_filename} 保存成功。")





