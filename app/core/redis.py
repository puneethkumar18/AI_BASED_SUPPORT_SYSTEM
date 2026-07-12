import redis

redis_client = redis.Redis(
    port=6379,
    host="localhost",
    decode_responses=True
)