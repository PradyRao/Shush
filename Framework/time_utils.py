import sys
import importlib

from datetime import datetime, timedelta, timezone

var_config = importlib.__import__("Config.var_config_" + sys.argv[1], fromlist=("var_config_" + sys.argv[1]))


def now_time():
    # This function just returns the current time
    # Timezone permanently set to UTC-5
    return int(datetime.now().astimezone(timezone(timedelta(hours=-5))).replace(microsecond=0).timestamp())


def now_date():
    return datetime.now().astimezone(timezone(timedelta(hours=-5))).replace(microsecond=0)


def time_practiced_seconds(voice_channel_id):
    return now_time() - var_config.practicemap[str(voice_channel_id) + 'start_time']


def time_readable(seconds):
    days = seconds // (24 * 3600)
    seconds %= (24 * 3600)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return [int(days), int(hours), int(minutes), int(seconds)]
