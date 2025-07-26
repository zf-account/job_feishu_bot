from fetchers.job_fetcher import fetch_jobs_within_24_hours
from senders.feishu_sender import send_to_feishu
from configs.config import JOB_SENDER_WEBHOOK_URL

if __name__ == "__main__":
    jobs = fetch_jobs_within_24_hours()
    if jobs:
        print(f"jobs is not null")
    send_to_feishu(jobs, JOB_SENDER_WEBHOOK_URL)
