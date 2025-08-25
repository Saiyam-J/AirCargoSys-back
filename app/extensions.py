from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
import os
import redis

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

redis_client = None

def init_redis(app):
    global redis_client
    url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    redis_client = redis.from_url(url, decode_responses=True)
    return redis_client
