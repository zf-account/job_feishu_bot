import requests
import os
import csv
from datetime import datetime, timedelta
from fetchers.hot_recommend_fetcher import fetch_jobs_with_hot_recommend

def get_jobs_ending_in_24h(path='jobs_data'):
    jobs = []
    now = datetime.now()
    next_24h = now + timedelta(hours=24)

    datetime_formats = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d']

    for filename in os.listdir(path):
        if filename.endswith('.csv'):
            with open(os.path.join(path, filename), 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    end_time_str = row.get('网申结束时间', '').strip()
                    end_time = None
                    for fmt in datetime_formats:
                        try:
                            end_time = datetime.strptime(end_time_str, fmt)
                            break
                        except ValueError:
                            continue
                    if not end_time:
                        continue
                    if now < end_time <= next_24h:
                        jobs.append(row)
    return jobs

def deadline_remind_sender(path, webhook_url):
    nums = 1
    jobs = get_jobs_ending_in_24h(path)
    if not jobs:
        content = "**未来24小时内没有公司截止投递**\n\n**下面推送热门推荐公司**\n\n"
        hot_recommend_jobs = fetch_jobs_with_hot_recommend()
        for job in hot_recommend_jobs:
            content += f"- [{nums} : {job['公司']} - {job['批次']}] \n    更新时间：{job['更新时间']} \n    网申开始时间：{job['网申开始时间']} \n    网申结束时间：{job['网申结束时间']}\n"
            nums += 1
    else:
        content = "**未来24小时内截止投递的公司如下：**\n\n"
        for job in jobs:
            content += f"- [{nums} : {job['公司']} - {job['批次']}] \n    更新时间：{job['更新时间']} \n    网申开始时间：{job['网申开始时间']} \n    网申结束时间：{job['网申结束时间']}\n"
            nums += 1

    data = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "未来24小时截止投递的公司",
                    "content": [
                        [{"tag": "text", "text": content}]
                    ]
                }
            }
        }
    }
    requests.post(webhook_url, json=data)


if __name__ == "__main__":
    jobs = get_jobs_ending_in_24h("jobs_data")
    for job in jobs:
        print(job)