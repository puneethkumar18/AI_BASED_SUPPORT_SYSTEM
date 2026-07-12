import json
from app.core.redis import redis_client

class CacheService:

    @staticmethod
    def get(key:str):
        value = redis_client.get(key)

        if value:
            return json.loads(value)
        
        return None
    
    @staticmethod
    def set(key:str,value,ttl: int = 300):
        redis_client.set(key,value,ttl)

    @staticmethod
    def delete(key:str):
        redis_client.delete(key)