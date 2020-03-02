from   collections import OrderedDict
from   datetime    import datetime, timezone

def iso8601(secs):
    return datetime.fromtimestamp(secs, timezone.utc).astimezone().isoformat()

def about_time(secs, nanosecs=None):
    about = OrderedDict()
    about["seconds"] = secs
    if nanosecs is not None:
        about["nanoseconds"] = nanosecs
    about["iso8601"] = iso8601(secs)
    return about
