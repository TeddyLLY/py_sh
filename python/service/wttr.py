from python.util.common import get_config , get_logger
from python.api.wttr import fetch_weather_to_string
import subprocess


logger = get_logger()
config = get_config()


def execute_shell(city):
    weather_data = fetch_weather_to_string(city)

  # 組合 shell 指令
    # echo "wttr.py.main()">> /tmp/taipei_weather.log
    cmd = f"{config.get('config', 'begin_command')} '{weather_data}' {config.get('config', 'end_command')}"

    # 執行 shell 指令
    subprocess.run(cmd, shell=True, check=True)


def get_wttr_str(city):
    return fetch_weather_to_string(city)