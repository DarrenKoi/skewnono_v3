import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

    # Redis settings
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    REDIS_DB = int(os.environ.get('REDIS_DB', 0))
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)

    # Scheduler settings
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = 'Asia/Seoul'

    # Resource limits for 2 CPU / 8GB environment
    MAX_THREADS = 4  # Limited thread pool
    MAX_PROCESSES = 2  # Limited process pool

    # Redis lock settings
    LOCK_EXPIRE_TIME = 3600  # 1 hour default
    LOCK_RETRY_TIMES = 3
    LOCK_RETRY_DELAY = 1