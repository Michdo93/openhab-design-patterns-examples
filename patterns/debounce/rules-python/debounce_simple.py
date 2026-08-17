import threading

from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger

timer = None


@rule(triggers=[ItemStateChangeTrigger("Person1PresenceSensor")])
class DebouncePerson1:
    def execute(self, module, input):
        global timer
        if timer is not None:
            timer.cancel()

        def on_expire():
            global timer
            sensor_state = Registry.getItem("Person1PresenceSensor").state
            proxy = Registry.getItem("Person1Presence")
            if str(proxy.state) != str(sensor_state):
                proxy.postUpdate(sensor_state)
            timer = None

        timer = threading.Timer(120, on_expire)
        timer.start()
