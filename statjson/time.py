from   collections import OrderedDict
from   datetime    import datetime
from   email.utils import localtime

def iso8601(secs):
    return localtime(datetime.fromtimestamp(secs)).isoformat()

def about_time(secs, nanosecs=None):
    about = OrderedDict()
    about["seconds"] = secs
    if nanosecs is not None:
        about["nanoseconds"] = nanosecs
    about["iso8601"] = iso8601(secs)
    return about
