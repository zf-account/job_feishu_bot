import logging
import os
import sys
import time

from configs.config import JOB_SENDER_WEBHOOK_URL
from configs.config import DEADLINE_REMIND_WEBHOOK_URL
from fetchers.job_fetcher import fetch_jobs_within_24_hours
from senders.feishu_sender import send_to_feishu
from senders.apply_deadline_remind_sender import deadline_remind_sender

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/aitotra/vscodeworkspace/job_feishu_bot/cron.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

if __name__ == "__main__":
    logging.info("Start execution daily_job_notifier.py")
    logging.info(f"Current working directory: {os.getcwd()}")
    logging.info(f"Python path: {sys.executable}")
    logging.info(f"Environment variable PATH: {os.environ.get('PATH', 'Not set')}")
    
    try:
        jobs = fetch_jobs_within_24_hours()
        logging.info(f"Get {len(jobs)} jobs")
        
        path = "/home/aitotra/vscodeworkspace/job_feishu_bot/jobs_data"
        logging.info(f"Data path: {path}")
        
        logging.info(f"JOB_SENDER_WEBHOOK_URL: {JOB_SENDER_WEBHOOK_URL[:20]}..." if JOB_SENDER_WEBHOOK_URL else "Not set")
        logging.info(f"DEADLINE_REMIND_WEBHOOK_URL: {DEADLINE_REMIND_WEBHOOK_URL[:20]}..." if DEADLINE_REMIND_WEBHOOK_URL else "Not set")
        
        logging.info("Start execution send_to_feishu...")
        send_to_feishu(jobs, JOB_SENDER_WEBHOOK_URL)
        logging.info("send_to_feishu execution completed")
        
        time.sleep(5) # Preventing frequency limiting

        logging.info("Start execution deadline_remind_sender...")
        deadline_remind_sender(path, DEADLINE_REMIND_WEBHOOK_URL)
        logging.info("deadline_remind_sender execution completed")
        
    except Exception as e:
        logging.error(f"Error occurred during execution: {str(e)}", exc_info=True)