"""
Created on 2021-07-07 19:35
@author: johannes
"""
import base64
import datetime
from threading import Thread


def get_time_now():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def get_base64(image_path):
    with open(image_path, "rb") as img_file:
        my_string = base64.b64encode(img_file.read()).decode("utf-8")
        return my_string


def thread_process(call_function, *args, **kwargs):
    Thread(target=call_function, args=args, daemon=True, kwargs=kwargs).start()
