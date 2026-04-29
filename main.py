import json
import os
import time

import dotenv
import requests
from loguru import logger

dotenv.load_dotenv()

URL = "https://hh.ru/applicant/resumes"
TOUCH_URL = f"https://{os.getenv('REGION')}hh.ru/applicant/resumes/touch"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": URL,
    "Origin": f"https://{os.getenv('REGION')}hh.ru",
    "X-Requested-With": "XMLHttpRequest",
    "X-XSRFToken": os.getenv("XSRF_TOKEN"),
    "Accept": "application/json",
}


def load_cookies():
    try:
        with open("cookies.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load cookies: {e}")
        return []


def get_cookies_value(name: str, data: list):
    return next((item["value"] for item in data if item["name"] == name), None)


def update():
    s = requests.Session()

    cookies = load_cookies()
    if not cookies:
        logger.warning("No content in cookies.json, waiting...")
        return None

    s.cookies.update({
        "hhtoken": get_cookies_value("hhtoken", cookies),
        "hhuid": get_cookies_value("hhuid", cookies),
        "_xsrf": os.getenv("XSRF_TOKEN"),
    })

    data = {
        "resume": os.getenv("RESUME_ID"),
        "undirectable": "true"
    }

    r = s.post(
        TOUCH_URL,
        headers=HEADERS,
        files={k: (None, v) for k, v in data.items()}
    )

    return r.status_code in [200, 409]


while True:
    ok = update()

    if ok is None:
        time.sleep(30)  # no cookies in cookies.json
        continue

    if not ok:
        logger.error("Update failed, waiting for another attempt...")
        time.sleep(60)
        continue

    logger.info("Your resume is at the top! Sleeping...")
    time.sleep(4.5 * 60 * 60)
