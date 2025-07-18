import sys
import traceback

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from python.util.common import get_logger , get_config
from python.service.wttr import execute_shell

config = get_config()
logger = get_logger()

#### add wanted cron task ####
def add_task(scheduler):

    scheduler.add_job(
        func=execute_shell,
        args=[config.get('config', 'city')],
        trigger='cron', hour=config.get('config', 'hour'), minute=config.get('config', 'min'), id='execute_shell'
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

    try:
        # add task
        scheduler = add_task(scheduler)
        scheduler.start()

        logger.info("Automation agent scheduler started. Press Ctrl+C to exit.")

    except (KeyboardInterrupt, SystemExit) as k:
        scheduler.shutdown()
        logger.error("Scheduler shut down.")
        logger.error(f"Exception occurred: {k}", exc_info=True)
    except Exception as e:
        logger.error("Scheduler broken.")
        logger.error(f"Exception occurred: {e}", exc_info=True)
    finally:
        formatted_traceback = traceback.format_exc()
        exc_type, exc_value, exc_traceback = sys.exc_info()

        if exc_value:
            logger.error("Final error message:")
            logger.error(f"{exc_type.__name__}: {exc_value}")
            logger.error(formatted_traceback)


if __name__ == "__main__":
    main()
