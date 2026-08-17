import threading
from datetime import datetime, timedelta

from openhab import rule, Registry
from openhab.triggers import ChannelEventTrigger

timers = {}
timestamps = {}


def switch_pressed(id_):
    timestamps[id_] = datetime.now().astimezone()
    Registry.getItem(id_).sendCommand("ON")

    def long_press_check():
        Registry.getItem(id_ + "LongPress").sendCommand("ON")
        Registry.getItem(id_ + "LongPress").sendCommand("OFF")
        pressed_at = timestamps.get(id_)
        if pressed_at and datetime.now().astimezone() < pressed_at + timedelta(seconds=5):
            t = threading.Timer(0.5, long_press_check)
            t.start()
            timers[id_] = t

    t = threading.Timer(0.5, long_press_check)
    t.start()
    timers[id_] = t


def switch_released(id_):
    if id_ in timers:
        timers[id_].cancel()
        del timers[id_]
    pressed = timestamps.pop(id_, None)

    if pressed and datetime.now().astimezone() < pressed + timedelta(milliseconds=500):
        Registry.getItem(id_ + "ShortPress").sendCommand("ON")
        Registry.getItem(id_ + "ShortPress").sendCommand("OFF")

    Registry.getItem(id_).sendCommand("OFF")


@rule(triggers=[ChannelEventTrigger("enocean:rockerSwitch:xxxxxxxx:xxxxxxxx:rockerswitchA")])
class Switch1Events:
    def execute(self, module, input):
        event_name = input.get("event")
        if event_name == "DIR1_PRESSED":
            switch_pressed("MySwitch1Up")
        elif event_name == "DIR1_RELEASED":
            switch_released("MySwitch1Up")
        elif event_name == "DIR2_PRESSED":
            switch_pressed("MySwitch1Down")
        elif event_name == "DIR2_RELEASED":
            switch_released("MySwitch1Down")
