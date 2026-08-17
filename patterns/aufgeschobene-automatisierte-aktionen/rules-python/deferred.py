import re

from openhab import Registry, logger
from openhab.actions import ScriptExecution
from datetime import datetime, timedelta

timers = {}

TIME_OFFSET = re.compile(r"^\+((?:\d+[hms])+)->(.*)$", re.IGNORECASE)
TIME_SPECIFIC = re.compile(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})->(.*)$")
DURATION_PART = re.compile(r"(\d+)([hms])", re.IGNORECASE)


def parse_offset(offset):
    total_seconds = 0
    for value, unit in DURATION_PART.findall(offset):
        value = int(value)
        unit = unit.lower()
        if unit == "h":
            total_seconds += value * 3600
        elif unit == "m":
            total_seconds += value * 60
        else:
            total_seconds += value
    return timedelta(seconds=total_seconds)


def set_deferred(target, raw_state):
    match = TIME_OFFSET.match(raw_state)
    if match:
        trigger_time = datetime.now().astimezone() + parse_offset(match.group(1))
        command = match.group(2)
    else:
        match = TIME_SPECIFIC.match(raw_state)
        if not match:
            raise ValueError("Ungueltiges Timerformat [" + raw_state + "]")
        trigger_time = datetime.fromisoformat(match.group(1)).astimezone()
        command = match.group(2)

    if trigger_time < datetime.now().astimezone():
        raise ValueError("Zielzeit liegt in der Vergangenheit")

    cancel_deferred(target)

    def on_expire():
        logger.info("Ausfuehren verzoegerter Aktion {} auf {}".format(command, target))
        del timers[target]
        Registry.getItem(target).sendCommand(command)

    timers[target] = ScriptExecution.createTimer(trigger_time, on_expire)


def cancel_deferred(target):
    if target in timers:
        timers[target].cancel()
        del timers[target]


def cancel_all():
    for target in list(timers.keys()):
        timers[target].cancel()
        del timers[target]
