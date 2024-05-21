
#521调试tk爬虫的断点的时候用的，没有完全更新完成的

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from openpyxl import Workbook
import psutil
import os
import subprocess
import time
import random


def open_browser():
    print("正在尝试启动浏览器...")
    # 检查 Chrome 是否已安装
    chrome_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
    print(f"Chrome路径：{chrome_path}")


    if not os.path.exists(chrome_path):
        print('启动程序错误，没有正确安装Chrome浏览器')
        exit(0)

    # 设置Chrome调试模式的数据存放路径（您的Google Chrome的用户数据目录）
    data_dir = r'C:\Users\shenlizhen\AppData\Local\Google\Chrome\User Data\Profile 2'

    # 通过子进程模式启动Chrome浏览器
    subprocess.Popen(f'"{chrome_path}" --remote-debugging-port=9527 --user-data-dir="{data_dir}"')

    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
    # 添加日志记录参数
    options.add_argument("--verbose")
    a = options.add_argument("--log-path=chrome.log")
    print(a)

    # 指定 chromedriver 的路径
    chromedriver_path = "D:\chromedriver-win64\chromedriver.exe"
    chromedriver_log_path = "chromedriver.log"
    chromedriver_log_level = "INFO"

    # 创建Chromedriver服务对象并设置日志路径和级别
    s = Service(chromedriver_path)
    s.log_path = chromedriver_log_path
    s.log_level = chromedriver_log_level

    # 创建Chromedriver实例时传入服务对象
    browser = webdriver.Chrome(service=s, options=options)

    browser.get("https://www.baidu.com")
    print("成功打开网页")



    # 返回浏览器对象
    return browser


def open_webpage(browser, keywords, desired_handles):
    print("开始打开网页...")
    base_search_url = "https://www.tiktok.com/search?q="
    total_links = []

    for keyword in keywords:
        print(f"正在搜索关键词 '{keyword}'...")
        search_url = base_search_url + keyword
        browser.get(search_url)
        time.sleep(8)

        current_keyword_links = set()
        no_new_links_count = 0
        prev_link_count = 0

        while len(current_keyword_links) < desired_handles:
            user_handles = []
            for i in range(desired_handles):
                try:
                    title_xpath = f'//*[@id="search_top-item-user-link-{i}"]/div/p'
                    title_element = browser.find_element(By.XPATH, title_xpath)
                    user_handles.append(title_element.text)
                except Exception as e:
                    print(f"获取标题时出错：{e}")
                    break

            base_url = "https://www.tiktok.com/@"
            for handle in user_handles:
                full_url = base_url + handle
                current_keyword_links.add(full_url)

            if len(current_keyword_links) == prev_link_count:
                no_new_links_count += 1
            else:
                no_new_links_count = 0

            prev_link_count = len(current_keyword_links)

            if no_new_links_count >= 5:
                print("连续多次滚动后链接数量未增加，退出循环。")
                break

            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            if len(current_keyword_links) >= desired_handles:
                print("已达到所需链接数量，退出循环。")
                break

        print(f"为关键词 '{keyword}' 收集到的链接数量：{len(current_keyword_links)}")
        total_links.extend(list(current_keyword_links))

    return total_links

def scrape_data(browser, total_links):
    data_list = []

    for link in total_links:
        browser.get(link)
        time.sleep(random.uniform(2, 5))

        try:
            fl_element = browser.find_element(By.XPATH,
                                              '//*[@id="main-content-others_homepage"]/div/div[1]/h3/div[2]/strong')
            flw = fl_element.text
            print(flw)

            try:
                click_element = browser.find_element(By.XPATH,
                                                     '//*[@id="main-content-others_homepage"]/div/div[2]/div[2]/div/div[1]/div[1]/div/div/a/div/div[2]/strong')
            except:
                click_element = browser.find_element(By.XPATH,
                                                     '//*[@id="main-content-others_homepage"]/div/div[2]/div[3]/div/div[1]/div[1]/div/div/a/div/div[2]/strong')

        except Exception as e:
            print(f"Error while trying to click: {e}")
            continue

        click_element.click()
        time.sleep(5)

        try:
            data_element = browser.find_element(By.XPATH,
                                                '//*[@id="app"]/div[2]/div[4]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/a[2]/span[2]/span[3]')
            datas = data_element.text
            print(datas)
            data_list.append([flw, link, datas])
        except Exception as e:
            print(f"Error while getting data: {e}")
            print(f"Error occurred at link: {link}")

        except Exception as e:
            print(f"Error while getting data after click: {e}")

    return data_list


def save_to_excel(data_list):
    wb = Workbook()
    ws = wb.active

    for data in data_list:
        ws.append(data)

    new_filename = get_new_filename()
    wb.save(new_filename)
    print(f"{new_filename} 保存成功。")


def close_all_excel():
    for process in psutil.process_iter():
        try:
            process_name = process.name()
            if process_name == "EXCEL.EXE":
                process.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def get_new_filename(base_name="1.xlsx"):
    counter = 1
    while os.path.exists(base_name):
        counter += 1
        base_name = f"{counter}.xlsx"
    return base_name


def main():
    close_all_excel()
    browser = open_browser()
    keywords = ["tiktoktips", "becomeaninfluencer", "smallbusinesstips"]
    desired_handles = 70

    total_links = open_webpage(browser, keywords, desired_handles)
    data_list = scrape_data(browser, total_links)
    save_to_excel(data_list)

def main():
    browser = open_browser()
    print("浏览器已成功启动")

if __name__ == "__main__":
    main()
