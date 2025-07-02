from flask import Flask, request
from python.util.common import get_config , get_logger
import pytz
from python.task.scheduler import main as scheduler
from python.service.wttr import get_wttr_str
from python.service.bench_cpu import bench_cpu_result
import threading
import time
from datetime import datetime

config = get_config()
app = Flask(__name__)
app.debug =  config.getboolean('config', 'APP_DEBUG_MODE')

tz = pytz.timezone("Asia/Taipei")
logger = get_logger()


@app.route('/')
def index():
    return 'Hello World!'


# ex : http://<host:port>/wttr?city=Tokyo
@app.route('/wttr')
def wttr():
    city = request.args.get('city', default='Taipei')
    return get_wttr_str(city)


# test cpu 餘數計算時間
@app.route('/bench_cpu')
def bench_cpu():
    count = int(request.args.get('count', default=10000000))

    return bench_cpu_result(count)

if __name__ == '__main__':
    try:
        threading.Thread(target=scheduler, daemon=True).start()
        app.run(host=config.get('config', 'APP_HOST'), port=int(config.get('config', 'APP_PORT')),threaded=True)


    except Exception as e:
        logger.error(f"Unhandled exception occurred: {e}", exc_info=True)