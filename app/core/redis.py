import redis
from app.core.config import settings

redis_client = redis.Redis(
    port=settings.REDIS_PORT,
    host=settings.REDIS_HOST,
    decode_responses=True
)