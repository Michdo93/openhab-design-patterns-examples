from datetime import datetime, timedelta

from openhab import rule
from openhab.triggers import ItemStateUpdateTrigger

until = None


@rule(triggers=[ItemStateUpdateTrigger("MyItem")])
class LatchedRule:
    def execute(self, module, input):
        global until
        now = datetime.now().astimezone()
        if until is not None and until > now:
            return  # Skip event if timer exists

        until = now + timedelta(days=1)

        # Regelcode ausfuehren
