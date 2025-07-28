import requests
import csv
from datetime import datetime
import time
from configs.config import HOT_RECOMMAND_COOKIES, HOT_RECOMMAND_HEADERS
def fetch_jobs_with_hot_recommand():
    cookies = HOT_RECOMMAND_COOKIES
    headers = HOT_RECOMMAND_HEADERS

    params = {
        '_': str(int(time.time() * 1000)),
    }

    data = {
    'cities': '',
    'industryIds': '',
    'query': '',
    'tab': '1',
    'propertyId': '',
    'batchId': '',
    'page': '1',
    'pageSize': '20',
    }

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
    now = int(time.time())
    for job in recruit_list:
        wangshenEndDate = int(job.get("wangshenEndDate", 0)) // 1000
        if wangshenEndDate >= now:
            jobs.append({
                "公司": job.get("name"),
                "批次": job.get("batchName"),
                "更新时间": datetime.fromtimestamp(int(job.get("wangshenUpdateTime", 0)) // 1000).strftime("%Y-%m-%d %H:%M"),
                "网申开始时间": datetime.fromtimestamp(job.get("wangshenBeginDate") / 1000).strftime("%Y-%m-%d %H:%M"),
                "网申结束时间": datetime.fromtimestamp(job.get("wangshenEndDate") / 1000).strftime("%Y-%m-%d %H:%M")
            })

    if jobs:
        filename = f"jobs_data/jobs_hot_recommand_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        fieldnames = list(jobs[0].keys())
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(jobs)

    return jobs

if __name__ == "__main__":
    jobs = fetch_jobs_with_hot_recommand()
    for job in jobs:
        print(job)