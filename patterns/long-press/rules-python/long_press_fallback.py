import threading

from datetime import datetime

from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger


def fallback_off():
    if str(Registry.getItem("ButtonState").state) == "ON":
        Registry.getItem("ButtonState").postUpdate("OFF")


@rule(triggers=[ItemStateChangeTrigger("ButtonState", state="ON", previous_state="OFF")])
class ButtonGedruecktMitFallback:
    def execute(self, module, input):
        global press_start
        press_start = datetime.now().astimezone()
        threading.Timer(5, fallback_off).start()
