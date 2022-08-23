from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()

start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

def get_date():
    print(today.strftime("%m-%d"))
    return today.strftime("%m-%d")
# get_date()


def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['low']), math.floor(weather['high'])
# get_weather()


def get_nowcity():
    return city
# get_nowcity()


def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days
# get_count()


def get_birthday():
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days
# get_birthday()


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']
# get_words()


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, low_temperature, high_temperature = get_weather()
data = {"weather": {"value": wea}, "min_temperature": {"value": low_temperature}, "max_temperature": {"value": high_temperature},
        "love_days": {"value": get_count()}, "city": {"value": get_nowcity()}, "date": {"value": get_date()},
        "birthday_left": {"value": get_birthday()}, "words": {"value": get_words(), "color": get_random_color()}}

res = wm.send_template(user_id, template_id, data)
print(res)