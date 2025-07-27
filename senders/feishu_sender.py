import requests
import csv
from datetime import datetime

def send_to_feishu(jobs, webhook_url):
    nums = 1
    # 新增：写入CSV
    if jobs:
        filename = f"jobs_data/jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        fieldnames = list(jobs[0].keys())
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(jobs)

    if not jobs:
        content = "**过去24小时内没有新职位更新**"
    else:
        content = "**过去24小时内更新的职位如下：**\n\n"
        for job in jobs:
            content += f"- [{nums} : {job['公司']} - {job['批次']}] \n    更新时间：{job['更新时间']} \n    网申开始时间：{job['网申开始时间']} \n    网申结束时间：{job['网申结束时间']}\n"
            nums += 1

    data = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "牛客校园招聘更新",
                    "content": [
                        [{"tag": "text", "text": content}]
                    ]
                }
            }
        }
    }
    requests.post(webhook_url, json=data)
