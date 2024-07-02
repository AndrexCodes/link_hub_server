from datetime import datetime

def ExtractTime(user_time=None):
    d = datetime.strptime(user_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    return [d.hour, d.minute]