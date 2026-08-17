from datetime import datetime, timedelta

from scope import cache

last_action = cache.privateCache.get("LastAction")
now = datetime.now().astimezone()

if last_action is None or last_action < now - timedelta(hours=24):
    print("Rate-limited action")
    cache.privateCache.put("LastAction", now)
