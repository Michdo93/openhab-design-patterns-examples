import threading

from datetime import datetime

from openhab import rule, Registry, logger
from openhab.triggers import ItemStateChangeTrigger


def fallback_off():
    if str(Registry.getItem("ButtonState").getState()) == "ON":
        logger.info("Fallback: no OFF signal received, resetting ButtonState manually")
        Registry.getItem("ButtonState").postUpdate("OFF")


@rule(triggers=[ItemStateChangeTrigger("ButtonState", state="ON", previous_state="OFF")])
class ButtonPressedWithFallback:
    def execute(self, module, input):
        threading.Timer(5, fallback_off).start()
