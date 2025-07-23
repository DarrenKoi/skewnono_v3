import redis
from redis import ConnectionPool
from config import Config

# Create a connection pool for better resource management
pool = ConnectionPool(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=Config.REDIS_DB,
    password=Config.REDIS_PASSWORD,
    max_connections=10,  # Limited connections for resource constraints
    decode_responses=True
)

def get_redis_client():
    """Get Redis client instance from pool"""
    return redis.Redis(connection_pool=pool)

# Global redis client
redis_client = get_redis_client()