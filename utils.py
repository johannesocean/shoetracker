"""
Created on 2021-07-07 19:35
@author: johannes
"""


def get_photo_id(list_len):
    return "abcdefghijklmnopqrstuvwxyz"[list_len]


def get_kilometers(miles=None):
    if miles:
        return round(miles * 1.609344, 2)
    else:
        return 0


def get_miles(km=None):
    if km:
        return round(km / 1.609344, 2)
    else:
        return 0
