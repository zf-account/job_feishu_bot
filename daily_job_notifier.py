from configs.config import JOB_SENDER_WEBHOOK_URL
from configs.config import DEADLINE_REMIND_WEBHOOK_URL
from fetchers.job_fetcher import fetch_jobs_within_24_hours
from senders.feishu_sender import send_to_feishu
from senders.apply_deadline_remind_sender import deadline_remind_sender

if __name__ == "__main__":
    jobs = fetch_jobs_within_24_hours()
    path = "/home/aitotra/vscodeworkspace/job_feishu_bot/jobs_data"
    send_to_feishu(jobs, JOB_SENDER_WEBHOOK_URL)
    deadline_remind_sender(path, DEADLINE_REMIND_WEBHOOK_URL)