from python.util.common import get_config , get_logger
import requests
import pytz
from datetime import datetime
import subprocess

logger = get_logger()
config = get_config()

def get_taiwan_us_time():
    # 定義時區
    tz_taiwan = pytz.timezone("Asia/Taipei")
    tz_us = pytz.timezone("America/New_York")

    # 取得當前時間（有時區資訊）
    now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
    time_taiwan = now_utc.astimezone(tz_taiwan)
    time_us = now_utc.astimezone(tz_us)

    # 格式化輸出
    return {
        "taiwan_time": time_taiwan.strftime("%Y-%m-%d %H:%M:%S %Z%z"),
        "us_time": time_us.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    }


## 取得今日天氣公開資料
# https://github.com/chubin/wttr.in
def fetch_weather_to_string(city="Taipei"):
    # url = f"https://wttr.in/{city}?format=j1"
    url = f"https://wttr.in/{city}?d"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return f"🌦️ {city}即時天氣（字串格式）：" + response.text
        else:
            return f"🌦️ 取得天氣失敗：Error {response.status_code}"
    except Exception as e:
        return f"🌦️ 取得天氣時發生錯誤：{e}"

def main(city):
    weather_data = fetch_weather_to_string(city)
    weather_data += get_taiwan_us_time()

  # 組合 shell 指令
    # echo "wttr.py.main()">> /tmp/taipei_weather.log
    cmd = f"{config.get('config', 'begin_command')} '{weather_data}' {config.get('config', 'end_command')}"

    # 執行 shell 指令
    subprocess.run(cmd, shell=True, check=True)

