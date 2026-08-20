from datetime import datetime

from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger

press_start = None


@rule(triggers=[ItemStateChangeTrigger("ButtonState", state="ON", previous_state="OFF")])
class ButtonGedrueckt:
    def execute(self, module, input):
        global press_start
        press_start = datetime.now().astimezone()


@rule(triggers=[ItemStateChangeTrigger("ButtonState", state="OFF", previous_state="ON")])
class ButtonLosgelassen:
    def execute(self, module, input):
        global press_start
        if press_start is None:
            return

        press_duration = (datetime.now().astimezone() - press_start).total_seconds() * 1000

        light = Registry.getItem("TargetLight")
        if press_duration < 500:
            light.sendCommand("OFF" if str(light.getState()) == "ON" else "ON")
            self.logger.info("Kurzer Druck ({:.0f}ms) -> Toggle".format(press_duration))
        else:
            light.sendCommand("INCREASE")
            self.logger.info("Langer Druck ({:.0f}ms) -> Dimmen".format(press_duration))

        Registry.getItem("ButtonPressTime").postUpdate(press_duration)
