from python.util.common import get_config , get_logger
import requests
from python.util.common import get_taiwan_us_time

logger = get_logger()
config = get_config()




## 取得今日天氣公開資料
# https://github.com/chubin/wttr.in
def fetch_weather_to_string(city="Taipei"):
    # url = f"https://wttr.in/{city}?format=j1"
    url = f"https://wttr.in/{city}?d"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return f"🌦️ {city}即時天氣（字串格式）：" + response.text + f" {get_taiwan_us_time()}"
        else:
            return f"🌦️ 取得天氣失敗：Error {response.status_code}"
    except Exception as e:
        return f"🌦️ 取得天氣時發生錯誤：{e}"
