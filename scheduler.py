import atexit
import logging

from Framework import scheduler_utils
from Tasks import reset_stats


def scheduler():
    atexit.register(at_exit)
    try:
        scheduler_utils.scheduler.start()
    except KeyboardInterrupt:
        logging.log('Got SIGTERM! Terminating...')


def at_exit():
    scheduler_utils.scheduler.remove_all_jobs()
    scheduler_utils.scheduler.shutdown(wait=False)


if __name__ == '__main__':
    scheduler()
