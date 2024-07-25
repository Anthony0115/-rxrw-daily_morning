from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

# 获取当前日期和时间
today = datetime.now()

# 从环境变量中获取相关信息
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

# 获取天气信息
def get_weather1():
    url = "http://v0.yiketianqi.com/free/v2030?city=&cityid=&adcode=130200000000&appid=76955423&appsecret=xRnKSP2r&lng=&lat=&aqi=&hours="
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        print("API响应:", data)  # 调试输出
        if 'data' in data and 'list' in data['data']:
            weather = data['data']['list'][0]
            return weather['wea'], math.floor(weather['tem'])
        else:
            print("API响应格式不正确或缺少预期的键")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None, None
    except KeyError as e:
        print(f"响应数据中缺少键: {e}")
        return None, None

# 计算从开始日期到今天的天数
def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days

# 计算下一个生日倒计时天数
def get_birthday():
    next_birthday = datetime.strptime(f"{date.today().year}-{birthday}", "%Y-%m-%d")
    if next_birthday < datetime.now():
        next_birthday = next_birthday.replace(year=next_birthday.year + 1)
    return (next_birthday - today).days

# 获取随机祝福语
def get_words():
    try:
        words = requests.get("https://api.shadiao.pro/chp")
        words.raise_for_status()
        return words.json()['data']['text']
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return "祝你开心每一天！"

# 获取随机颜色
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)

# 初始化WeChat客户端
client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)

# 获取天气信息
wea, temperature = get_weather1()
if wea is not None and temperature is not None:
    # 准备数据并发送模板消息
    data = {
        "weather": {"value": wea},
        "temperature": {"value": temperature},
        "love_days": {"value": get_count()},
        "birthday_left": {"value": get_birthday()},
        "words": {"value": get_words(), "color": get_random_color()}
    }
    res = wm.send_template(user_id, template_id, data)
    print(res)
else:
    print("无法获取天气信息，模板消息未发送")
