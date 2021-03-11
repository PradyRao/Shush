from datetime import datetime, timedelta, timezone

from Config import var_config


def now_time():
    # This function just returns the current time
    # Timezone permanently set to UTC-5
    return int(datetime.now().astimezone(timezone(timedelta(hours=-5))).replace(microsecond=0).timestamp())


def time_practiced_seconds(voice_channel_id):
    return now_time() - var_config.practicemap[str(voice_channel_id) + 'start_time']


def time_readable(seconds):
    days = seconds // (24 * 3600)
    seconds %= (24 * 3600)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return [days, hours, minutes, seconds]
