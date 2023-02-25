from flet import Icon
import base64
import datetime
from threading import Thread


def get_time_now():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def get_base64(image_path):
    with open(image_path, "rb") as img_file:
        my_string = base64.b64encode(img_file.read()).decode("utf-8")
        return my_string


def get_distance_icon(distance):
    if distance is None:
        return Icon()
    if distance < 600:
        return Icon(name="check_circle", color="green")
    elif distance < 900:
        return Icon(name="warning_rounded", color="yellow")
    else:
        return Icon(name="do_not_disturb_on_rounded", color="red")


def thread_process(call_function, *args, **kwargs):
    Thread(target=call_function, args=args, daemon=True, kwargs=kwargs).start()
