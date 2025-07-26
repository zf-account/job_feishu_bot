import requests
import datetime
import time
from configs.config import COOKIES, HEADERS
def fetch_jobs_within_24_hours():
    cookies = COOKIES
    headers = HEADERS
    params = {
        '_': str(int(time.time() * 1000)),
    }

    data = {
        'query': '',
        'propertyId': '',
        'page': '1',
        'pageSize': '20',
        'tab': '3',
    }

    now = int(time.time())
    yesterday = now - 86400
    jobs = []

    response = requests.post(
        'https://www.nowcoder.com/np-api/u/school-schedule/list-card',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
        timeout=10
    )
    print("状态码:", response.status_code)
    result = response.json()
    recruit_list = result.get('data').get('datas')
    for job in recruit_list:
        update_time = int(job.get("wangshenUpdateTime", 0)) // 1000
        if update_time >= yesterday:
            jobs.append({
                "公司": job.get("name"),
                "批次": job.get("batchName"),
                "更新时间": datetime.datetime.fromtimestamp(update_time).strftime("%Y-%m-%d %H:%M"),
                "网申开始时间": datetime.datetime.fromtimestamp(job.get("wangshenBeginDate") / 1000).strftime("%Y-%m-%d %H:%M"),
                "网申结束时间": datetime.datetime.fromtimestamp(job.get("wangshenEndDate") / 1000).strftime("%Y-%m-%d %H:%M")
            })
    return jobs

if __name__ == "__main__":
    jobs = fetch_jobs_within_24_hours()
    for job in jobs:
        print(job)