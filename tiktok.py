#爬取tk某部分数据
import os
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 检查 Chrome 是否已安装
chrome_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
if not os.path.exists(chrome_path):
    print('启动程序错误，没有正确安装Chrome浏览器')
    exit(0)

# 设置Chrome调试模式的数据存放路径
data_dir = r'D:\youbafu\selenium'
os.makedirs(data_dir, exist_ok=True)

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

browser.get('https://www.tiktok.com/search?q=cola&t=1697633816334')
time.sleep(2)  # 等待页面初步加载

# 循环滚动页面
for _ in range(10):  # 可以根据需要调整滚动次数
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # 等待页面加载

    # 获取标题文本
    user_handles = []
    for i in range(50):  # 预估的最大数量，可以根据需要调整
        try:
            title_xpath = f'//*[@id="search_top-item-user-link-{i}"]/div/p'
            title_element = browser.find_element(By.XPATH, title_xpath)
            user_handles.append(title_element.text)
        except:
            break

    # 构造完整链接并打印
    base_url = "https://www.tiktok.com/@"
    for handle in user_handles:
        full_url = base_url + handle
        print(full_url)

browser.quit()
