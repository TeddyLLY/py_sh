import sys
import traceback

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
import time
from python.util.common import get_logger , get_config
from python.api.wttr import fetch_weather_to_string

config = get_config()
logger = get_logger()

#### add wanted cron task ####
def add_task(scheduler):

    scheduler.add_job(
        func=fetch_weather_to_string,
        args=[config.get('config', 'city')],
        trigger='cron', hour=config.get('config', 'hour'), minute=config.get('config', 'min'), id='automation_agent_monitor_disk_usage'
    )

    return scheduler
#### ####




def main():
    # Setup scheduler with a process pool
    executors = {
        # ops 機器 cpu 一般都不會很多
        # 使用虛擬 thread ThreadPoolExecutor , 取代實體 cpu mutil core 執行 ProcessPoolExecutor
        # 'default': ProcessPoolExecutor(max_workers=1)
        'default': ThreadPoolExecutor(max_workers=1)
    }
    job_defaults = {
        'coalesce': True,
        'misfire_grace_time': None
    }
    scheduler = BackgroundScheduler( job_defaults=job_defaults, executors=executors)

    # add task
    scheduler = add_task(scheduler)
    scheduler.start()

    logger.info("Automation agent scheduler started. Press Ctrl+C to exit.")

    try:
        while True:
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit) as k:
        scheduler.shutdown()
        logger.error("Scheduler shut down.")
        logger.error(f"Exception occurred: {k}", exc_info=True)
    except Exception as e:
        logger.error("Scheduler broken.")
        logger.error(f"Exception occurred: {e}", exc_info=True)
    finally:
        exc_type, exc_value, exc_traceback = traceback.format_exc(), *sys.exc_info()
        if exc_value:
            logger.error("Final error message:")
            logger.error(exc_value)


if __name__ == "__main__":
    main()
