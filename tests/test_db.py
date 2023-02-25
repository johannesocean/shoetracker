# import redis
# import pickle
# import time
# import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
# start_time = time.time()
# r = redis.Redis(
#   host=os.getenv('DB_HOST'),
#   port=os.getenv('DB_PORT'),
#   password=os.getenv('DB_PASS'),
#   ssl=True
# )
# start_time = time.time()
# print(r.keys())
# print("Timeit:--%.5f sec" % (time.time() - start_time))
#
# # pickle.loads(r.get('shoes'))
# #
# for key in r.keys():
#     r.delete(key)
