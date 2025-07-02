from configparser import ConfigParser
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import pytz
from datetime import datetime

global_config = None
global_logger = None


def get_pypath(str):
    return os.path.join(os.environ.get("PYTHONPATH", ""),str)

def get_config():
    global global_config
    if global_config == None:
        global_config = ConfigParser()
        global_config.read(get_pypath('config/config.ini'))
    return global_config


def get_logger():
    global global_logger
    if global_logger == None:
        config = get_config()

        log_date_format = '%Y-%m-%d %H:%M:%S'
        log_path = get_pypath(config.get("config", "log_path"))
        # 建立log資料夾 (if not exist)
        os.makedirs(log_path, exist_ok=True)
        log_name = config.get("config", "log_name")
        log_mode = config.get("config", "log_mode")
        log_level = config.get("config", "log_level")
        log_path_name = log_path + '/' + log_name
        logging.basicConfig(
                                level=log_level,  # 起跳log等級
                                filemode=log_mode,  # log檔開啟模式
                                format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                                datefmt=log_date_format  # 設定時間格式
                            )
        global_logger = logging.getLogger(__name__)

        handler = TimedRotatingFileHandler(
            filename=log_path_name,
            when="midnight",
            interval=1,
            backupCount=0,
            encoding="utf-8"
        )

        # 設定 log 檔案格式
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s', log_date_format)
        handler.setFormatter(formatter)

        handler.suffix = "%Y-%m-%d_%H-%M-%S.log"
        global_logger.addHandler(handler)

    return global_logger

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