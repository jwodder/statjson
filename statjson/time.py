from   collections import OrderedDict
from   datetime    import datetime
import time

def iso8601(secs):
    stamp = datetime.fromtimestamp(secs).isoformat()
    local = time.localtime(secs)
    offset = time.altzone if local.tm_isdst else time.timezone
    if offset <= 0:
        stamp += '+'
        offset *= -1
    else:
        stamp += '-'
    stamp += '{:02}:{:02}'.format(*divmod(offset // 60, 60))
    return stamp

def about_time(secs, nanosecs=None):
    about = OrderedDict()
    about["seconds"] = secs
    if nanosecs is not None:
        about["nanoseconds"] = nanosecs
    about["iso8601"] = iso8601(secs)
    return about
