from job_fetcher import fetch_jobs_within_24_hours
from feishu_sender import send_to_feishu
from config import WEBHOOK_URL

if __name__ == "__main__":
    jobs = fetch_jobs_within_24_hours()
    send_to_feishu(jobs, WEBHOOK_URL)
