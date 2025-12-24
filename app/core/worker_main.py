import time
from app.core.worker import executor
from app.core.logger import logger

# Worker process stays alive
if __name__ == "__main__":
    logger.info("Worker started, waiting for jobs...")
    while True:
        time.sleep(5)