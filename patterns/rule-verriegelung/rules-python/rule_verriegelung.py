from datetime import datetime, timedelta

from openhab import rule, logger
from openhab.triggers import ItemStateUpdateTrigger

until = None


@rule(triggers=[ItemStateUpdateTrigger("MyItem")])
class LatchedRule:
    def execute(self, module, input):
        global until
        now = datetime.now().astimezone()
        if until is not None and until > now:
            logger.info("Event ignored, locked until " + str(until))
            return  # Ereignis überspringen, solange die Sperre aktiv ist

        until = now + timedelta(days=1)
        logger.info("Rule code executed, locked until " + str(until))
        # Regelcode ausführen
