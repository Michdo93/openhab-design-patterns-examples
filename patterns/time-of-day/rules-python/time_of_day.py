from datetime import datetime

from openhab import rule, Registry
from openhab.triggers import GenericCronTrigger, SystemStartlevelTrigger

TIMES_OF_DAY = {
    "week": [
        ("MORNING",   "07:05", "12:00"),
        ("AFTERNOON", "12:00", "19:00"),
        ("EVENING",   "19:00", "23:00"),
        ("NIGHT",     "23:00", "24:00"),
    ],
    "saturday": [
        ("MORNING",   "08:00", "12:00"),
        ("AFTERNOON", "12:00", "19:00"),
        ("EVENING",   "19:00", "23:30"),
        ("NIGHT",     "23:30", "24:00"),
    ],
    "sunday": [
        ("MORNING",   "08:30", "12:00"),
        ("AFTERNOON", "12:00", "18:00"),
        ("EVENING",   "18:00", "22:30"),
        ("NIGHT",     "22:30", "24:00"),
    ],
}


def min_of_day(s):
    hour, minute = (int(part) for part in s.split(":"))
    return hour * 60 + minute


@rule(
    name="Set vTimeOfDay",
    triggers=[
        SystemStartlevelTrigger(100),
        GenericCronTrigger("0 * * * * ?"),
    ],
)
class SetVTimeOfDay:
    def execute(self, module, input):
        now = datetime.now()
        now_mod = now.hour * 60 + now.minute
        weekday = now.isoweekday()  # 1=Montag ... 7=Sonntag
        table = (
            TIMES_OF_DAY["sunday"] if weekday == 7
            else TIMES_OF_DAY["saturday"] if weekday == 6
            else TIMES_OF_DAY["week"]
        )

        prev = Registry.getItem("vTimeOfDay").getState()
        curr = "UNKNOWN"

        for state, start_str, end_str in table:
            start = min_of_day(start_str)
            end = min_of_day(end_str)
            if start <= now_mod < end:
                curr = state
                break

        if curr != str(prev):
            Registry.getItem("vTimeOfDay").sendCommand(curr)
            self.logger.info("vTimeOfDay -> " + curr)
