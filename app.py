from flask import Flask
from python.util.common import get_config , get_logger
import pytz
from python.task.scheduler import main as scheduler

config = get_config()
app = Flask(__name__)
app.debug = config.get('config', 'APP_DEBUG_MODE')

tz = pytz.timezone("Asia/Taipei")
logger = get_logger()


@app.route('/')
def index():
    return 'Hello World!'


if __name__ == '__main__':
    try:
        app.run(host=config.get('config', 'APP_HOST'), port=config.get('config', 'APP_PORT'),threaded=True)
        scheduler()

    except Exception as e:
        logger.error(f"Unhandled exception occurred: {e}", exc_info=True)