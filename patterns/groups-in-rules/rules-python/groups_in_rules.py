from datetime import datetime

from openhab import rule, Registry
from openhab.triggers import GroupStateChangeTrigger, GroupStateUpdateTrigger


@rule(triggers=[GroupStateChangeTrigger("gDoorsSensors")])
class ADoorSensorChanged:
    def execute(self, module, input):
        event = input.get("event")
        if not event:
            return

        door = Registry.getItem(event.getItemName())
        timer = Registry.getItem(door.getName() + "_Timer")
        last_update = Registry.getItem(door.getName() + "_LastUpdate")

        door_state = str(door.getState())

        if door_state == "OPEN":
            timer.sendCommand("ON")
        else:
            timer.postUpdate("OFF")

        last_update.postUpdate(datetime.now().astimezone())

        msg = door.getName() + (" was opened" if door_state == "OPEN" else " was closed")

        alert = False
        time_of_day = str(Registry.getItem("vTimeOfDay").getState())
        if time_of_day in ("NIGHT", "BED"):
            alert = True
            msg += " at night"
        if str(Registry.getItem("vPresent").getState()) == "OFF":
            alert = True
            msg += " and no one is home"

        if alert:
            Registry.getItem("aAlerts").sendCommand(msg)
        self.logger.info(msg)


@rule(triggers=[GroupStateUpdateTrigger("gDoorsTimers", "OFF")])
class TimerExpiredForADoor:
    def execute(self, module, input):
        event = input.get("event")
        if not event:
            return

        item_name = event.getItemName()
        door_name = item_name.split("_")[0]

        open_doors = [
            d.getName() for d in Registry.getItem("gDoorsSensors").getAllMembers()
            if str(d.getState()) == "OPEN"
        ]

        msg = door_name + " has been open for over an hour"
        if open_doors:
            msg += " and also open: " + ", ".join(open_doors)

        Registry.getItem("aAlerts").sendCommand(msg)
        self.logger.info(msg)

        time_of_day = str(Registry.getItem("vTimeOfDay").getState())
        if time_of_day in ("NIGHT", "BED"):
            Registry.getItem(item_name).sendCommand("ON")
