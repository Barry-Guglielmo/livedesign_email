import datetime
import json
import pytz
from config import *

# format the date time log_file location in config
data_list = []
with open(log_file, 'r') as file:
    # Read the content of the file
    file_content = file.read()
    data_list = json.loads(file_content)

def last_log():
    data_list = []
    with open(log_file, 'r') as file:
        # Read the content of the file
        file_content = file.read()
        data_list = json.loads(file_content)
    return data_list['cdd_last_sync'][0]['last_sync_datetime']

def check_logs(threshold_hours):
    # note the current cdd sync log script uses utc
    delta = datetime.timedelta(hours=-8)
    last_sync_utc = last_log()[:-4]
    last_sync_utc = datetime.datetime.strptime(last_sync_utc, '%Y-%m-%d %H:%M:%S')
    last_sync_pst = last_sync_utc + delta
    current_time_utc = datetime.datetime.now(pytz.utc)
    current_time_utc = current_time_utc.strftime('%Y-%m-%d %H:%M:%S')
    current_time_utc = datetime.datetime.strptime(current_time_utc, '%Y-%m-%d %H:%M:%S')
    current_time_pst = current_time_utc + delta

    time_difference = current_time_utc - last_sync_utc

    if time_difference > datetime.timedelta(hours=threshold_hours):
        return [True, time_difference]
    else:
        return [False, time_difference]
