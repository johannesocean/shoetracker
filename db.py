import os
import redis
# from dotenv import load_dotenv
#
# load_dotenv()


def get_db():
    try:
        if os.getenv('DB_HOST'):
            return redis.Redis(
                host=os.getenv('DB_HOST'),
                port=int(os.getenv('DB_PORT')),
                password=os.getenv('DB_PASS'),
                ssl=True
            )
    except BaseException:
        return None
    finally:
        return None


def write_to_db(*args, **kwargs):
    db = get_db()
    if db:
        for key, item in kwargs.items():
            db.set(key, item)
