from datetime import datetime, timezone

def utc():
    # Get the current UTC time
    utc_time = datetime.utcnow().replace(tzinfo=timezone.utc)
    return utc_time
