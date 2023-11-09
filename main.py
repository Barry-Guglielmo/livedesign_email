from body import *
from check_logs import *
from ld_email import *
from config import *
from datetime import timedelta

# IF CDD FAILED TO RUN AFTER SET TIME SEND EMAIL
sync = check_logs(max_time)
if sync[0]:
    # convert from utc to pst
    last_sync_pst = datetime.datetime.strptime(last_log()[:-4], '%Y-%m-%d %H:%M:%S') + timedelta(hours=-8)
    text = """
The last sync was at %s PST. It has been %s hours since last sync.<br>
"""%(last_sync_pst, sync[1])
    for email in to_addrs:
        send_email(email, email_title, body(text))
