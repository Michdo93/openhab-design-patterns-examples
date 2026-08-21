import threading

from openhab import rule, Registry, logger
from openhab.triggers import ItemStateChangeTrigger

timer = None


@rule(triggers=[ItemStateChangeTrigger("Person1PresenceSensor")])
class DebouncePerson1:
    def execute(self, module, input):
        global timer
        if timer is not None:
            timer.cancel()

        sensor_state = str(Registry.getItem("Person1PresenceSensor").getState())
        delay_seconds = 0 if sensor_state == "ON" else 120

        def on_expire():
            global timer
            proxy = Registry.getItem("Person1Presence")
            if str(proxy.getState()) != sensor_state:
                proxy.postUpdate(sensor_state)
                logger.info(
                    "Person1Presence uebernimmt {} (Verzoegerung={}s)".format(sensor_state, delay_seconds)
                )
            timer = None

        timer = threading.Timer(delay_seconds, on_expire)
        timer.start()
