import redis
from django.conf import settings

# redis_server = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
redis_server = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
