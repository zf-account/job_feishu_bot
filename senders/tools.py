import requests
import logging
import time
def send_with_retry(request_func, max_retries=3, base_delay=3):
    for attempt in range(max_retries):
        try:
            response = request_func()
            if response.status_code == 200:
                resp_json = response.json()
                if resp_json.get('code') == 0:
                    return resp_json  # 成功
                elif resp_json.get('code') == 11232:
                    logging.warning(f"Rate limited, retrying in {base_delay * (attempt + 1)}s...")
                    time.sleep(base_delay * (attempt + 1))
                else:
                    logging.error(f"Feishu API error: {resp_json}")
                    return None
            else:
                logging.error(f"HTTP error: {response.status_code}")
                return None
        except Exception as e:
            logging.error(f"Request failed: {str(e)}", exc_info=True)
            time.sleep(base_delay * (attempt + 1))
    logging.error("Max retries exceeded.")
    return None
