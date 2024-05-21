

#爬取混豚数据
import requests
import pandas as pd
import json

# 定义请求的 URL 和 headers
url = "https://www.shoplus.net/api/v1/rank/product_rising_rank?cycle=H24&is_commerce=false&version=H24-2023102900-2023103100&country_code=GB&cursor=1&sort=10&size=20"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Cookie": "Hm_lvt_51956877b2ac5aabc38d224aa78a05d8=1698720181; Hm_lpvt_51956877b2ac5aabc38d224aa78a05d8=1698720181; _clck=gn6zxs|2|fgb|0|1399; _ga=GA1.1.1625217483.1698720186; __root_domain_v=.huitun.com; _qddaz=QD.179998720186246; SESSION=ZjE2YjQ2ZWUtZjViNi00Zjg0LWEwNWMtNDVhNjJlZmMzYWM4; _clsk=18vs1jb|1698720201121|3|1|p.clarity.ms/collect; _ga_JBKBWWH0KV=GS1.1.1698720186.1.1.1698720341.0.0.0"
}

# 发送 GET 请求
response = requests.get(url, headers=headers)

# 检查响应状态if response.status_code == 200:
# 解析 JSON 数据
data = json.loads(response.text)

# 提取 extData
ext_data = data.get("extData", [])

# 转换为 DataFrame
df = pd.DataFrame(ext_data)

# 保存为 CSV 文件（或其他格式）
df.to_csv("extData.csv", index=False)