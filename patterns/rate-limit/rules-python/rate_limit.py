from datetime import datetime, timedelta

from openhab import rule
from openhab.triggers import ItemCommandTrigger
from scope import cache


@rule(triggers=[ItemCommandTrigger("RateLimitTrigger", "ON")])
class RateLimitBeispiel:
    def execute(self, module, input):
        last_action = cache.privateCache.get("LastAction")
        now = datetime.now().astimezone()

        if last_action is None or last_action < now - timedelta(hours=24):
            self.logger.info("Rate-limited action")
            cache.privateCache.put("LastAction", now)
        else:
            self.logger.info("Ereignis ignoriert, Sperrzeit laeuft noch")
