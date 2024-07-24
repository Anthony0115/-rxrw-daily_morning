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


def get_weather1():
  url = "http://v1.yiketianqi.com/api?unescape=1&version=v91&appid=&{76955423}appsecret=${xRnKSP2r}&unescape=1&cityid=${101220501}"
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])
def get_weather():
    app_id = '76955423'  # 你的 appId
    app_secret = 'xRnKSP2r'  # 你的 appSecret
    city_id = '101220501'  # 马鞍山的城市 ID

    url = f"http://v1.yiketianqi.com/free/day??appid={app_id}&appsecret={app_secret}&unescape=1&cityid={city_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()
        
        # 检查响应中是否包含期望的数据
        if 'wea' in data and 'tem_night' in data and 'tem_day' in data:
            return {
                'wea': data['wea'],
                'low': data['tem_night'],
                'high': data['tem_day']
            }
        else:
            raise ValueError("响应结构中缺少必要的数据")
    except requests.RequestException as e:
        print(f"获取天气信息失败: {e}")
        return None
def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
data = {"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
