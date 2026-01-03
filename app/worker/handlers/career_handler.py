from playwright.sync_api import sync_playwright
from app.worker.logger import logger
import sqlite3
import datetime
import os
def fetch_opportunities():
    scrape_linkedin()

def scrape_linkedin():
    search_url="https://www.linkedin.com/jobs/search/?currentJobId=4349880985&f_TPR=r86400&keywords=software%20engineer&location=India"
    logger.info(f"PLAYWRIGHT_BROWSERS_PATH before browser {os.getenv('PLAYWRIGHT_BROWSERS_PATH')}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True,args=["--no-sandbox", "--disable-setuid-sandbox"])
        page = browser.new_page()

    #     page.goto(search_url, timeout=60000)