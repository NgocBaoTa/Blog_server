import datetime
import pytz
from tzlocal import get_localzone

local_tz = get_localzone()

def convert_to_utc_time():
    current_datetime_utc = datetime.datetime.now(tz = pytz.utc)
    current_timestamp = current_datetime_utc.timestamp()
    return current_timestamp


def convert_to_local_time(utc_time):
    naive_datetime = datetime.datetime.utcfromtimestamp(utc_time)
    utc_date = pytz.utc.localize(naive_datetime)
    local_time = utc_date.astimezone(pytz.timezone(str(local_tz))).strftime("%Y-%m-%d %H:%M")
    return local_time