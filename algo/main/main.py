import pandas as pd
import pywencai as wc
import requests
import json
from bs4 import BeautifulSoup

# 问财url
wencai_url = 'https://www.iwencai.com/customized/chart/get-robot-data'

cookie = 'other_uid=Ths_iwencai_Xuangu_e7elqiflf0549zsdju04denlkds27cqb; ta_random_userid=jt280gfpfi; cid=84355f56d0f44927a9fe4135cc3964741704199870; cid=84355f56d0f44927a9fe4135cc3964741704199870; ComputerID=84355f56d0f44927a9fe4135cc3964741704199870; WafStatus=0; ttype=WEB; user=MDptb181NjI3MjgwNzU6Ok5vbmU6NTAwOjU3MjcyODA3NTo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNDo6OjU2MjcyODA3NToxNzA4MzUyMzM4Ojo6MTYxMDkyNDk0MDo2MDQ4MDA6MDoxNjU3ODAyOWQ4ZDk0OWQ1ZTQ5NzU2ODI2NmY2NTU1OGQ6ZGVmYXVsdF80OjE%3D; userid=562728075; u_name=mo_562728075; escapename=mo_562728075; ticket=9c0698b659a91649b0adc96071e81e9f; user_status=0; utk=7e541748b898407b504ae6cf6a720a91; v=AywVK-56ZUPbW3EQQdMr-ruV_QFb5fN20oLkUYZvO0Z6gsI_rvWgHyKZtMzV'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    # 'Content-Length': 0,
    'Content-Type': 'application/json',
    'Cookie': cookie,
    'Hexin-V': 'AywVK-56ZUPbW3EQQdMr-ruV_QFb5fN20oLkUYZvO0Z6gsI_rvWgHyKZtMzV',
    }


def ask_question(question: str):
    add_info = {'urp': {'scene': 1, 'company': 1, 'business': 1, 'contentType': 'json', 'searchInfo': True}}
    log_info = {'input_type': "typewrite"}
    json_obj = {'add_info': json.dumps(add_info),
                'block_list': "",
                'log_info': json.dumps(log_info),
                'page': 1,
                'perpage': 50,
                'query_area': "",
                'question': question,
                'rsh': "562728075",
                'secondary_intent': "stock",
                'source': 'Ths_iwencai_Xuangu',
                'version': "2.0"
                }

    r = requests.post(wencai_url, json=json_obj, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    print(soup)


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # ask_question("小盘股,剔除ST")
# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
    df = pd.DataFrame()
    df.to_csv('abc\cc.csv', encoding='utf-8-sig', index=None)
