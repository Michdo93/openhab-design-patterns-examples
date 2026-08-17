import threading

from openhab import rule, Registry
from openhab.triggers import (
    SystemStartlevelTrigger,
    GenericCronTrigger,
    ItemCommandTrigger,
)

irrigation_timer = None


def item_exists(name):
    try:
        return Registry.getItem(name) is not None
    except Exception:
        return False


@rule(triggers=[SystemStartlevelTrigger(100)])
class IrrigationResetBeiSystemstart:
    def execute(self, module, input):
        for valve in Registry.getItem("gIrrigation").members:
            if str(valve.state) != "OFF":
                valve.sendCommand("OFF")
        Registry.getItem("Irrigation_Curr").postUpdate("OFF")


@rule(triggers=[
    GenericCronTrigger("0 0 8 * * ?"),
    ItemCommandTrigger("Irrigation_Manual", "ON"),
])
class IrrigationStartUm0800:
    def execute(self, module, input):
        received = input.get("command")
        if str(Registry.getItem("Irrigation_Auto").state) == "ON" or received == "ON":
            Registry.getItem("Irrigation_Manual").postUpdate("ON")
            self.logger.info("Bewaesserung gestartet, Zone 1 aktiv")
            Registry.getItem("Irrigation_Curr").sendCommand("Irrigation_Zone_1")


@rule(triggers=[ItemCommandTrigger("Irrigation_Curr")])
class IrrigationCascade:
    def execute(self, module, input):
        global irrigation_timer
        curr_valve_name = input["command"]
        curr_valve = Registry.getItem(curr_valve_name)
        curr_valve_num = int(curr_valve_name.split("_")[2])
        curr_valve_mins = int(str(Registry.getItem(curr_valve_name + "_Time").state))
        next_valve_name = "Irrigation_Zone_" + str(curr_valve_num + 1)

        curr_valve.sendCommand("ON")

        def on_expire():
            global irrigation_timer
            self.logger.info("Zone " + curr_valve_name + " aus")
            curr_valve.sendCommand("OFF")

            if item_exists(next_valve_name):
                self.logger.info("Zone " + next_valve_name + " an")
                Registry.getItem("Irrigation_Curr").sendCommand(next_valve_name)
            else:
                self.logger.info("Bewaesserung abgeschlossen")
                Registry.getItem("Irrigation_Manual").sendCommand("OFF")
            irrigation_timer = None

        irrigation_timer = threading.Timer(curr_valve_mins * 60, on_expire)
        irrigation_timer.start()


@rule(triggers=[ItemCommandTrigger("Irrigation_Manual", "OFF")])
class IrrigationCancel:
    def execute(self, module, input):
        global irrigation_timer
        if irrigation_timer is not None:
            irrigation_timer.cancel()
            irrigation_timer = None

        for valve in Registry.getItem("gIrrigation").members:
            if str(valve.state) != "OFF":
                valve.sendCommand("OFF")
        Registry.getItem("Irrigation_Curr").postUpdate("OFF")
