import os
import redis
import pickle
# from dotenv import load_dotenv
#
# load_dotenv()


def get_db():
    try:
        return redis.Redis(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            password=os.getenv('DB_PASS'),
            ssl=True
        )
    except BaseException:
        return None


def read_from_db(key):
    db = get_db()
    if db:
        try:
            data = db.get(key)
            return pickle.loads(data)
        except:
            ...


def write_to_db(*args, **kwargs):
    db = get_db()
    if db:
        for key, item in kwargs.items():
            db.set(key, pickle.dumps(item))
