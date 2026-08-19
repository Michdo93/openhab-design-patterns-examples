import threading

from openhab import rule, Registry, logger
from openhab.triggers import ItemCommandTrigger

dim_timer = None
continue_dimming = True


def step():
    global dim_timer, continue_dimming

    lamp_state = str(Registry.getItem("DimLamp").getState())
    target_state = str(Registry.getItem("DimTarget").getState())
    curr_level = int(lamp_state) if lamp_state not in ("NULL", "UNDEF") else 0
    target = int(target_state) if target_state not in ("NULL", "UNDEF") else 0

    if curr_level >= target or not continue_dimming:
        logger.info("Dimmen beendet bei {}%".format(curr_level))
        dim_timer = None
        return

    Registry.getItem("DimLamp").sendCommand(curr_level + 1)
    dim_timer = threading.Timer(1, step)
    dim_timer.start()


@rule(triggers=[ItemCommandTrigger("StartDimTrigger", "ON")])
class StartDimming:
    def execute(self, module, input):
        global continue_dimming
        continue_dimming = True
        self.logger.info("Dimmen gestartet")
        step()


@rule(triggers=[ItemCommandTrigger("CancelDimTrigger", "ON")])
class CancelDimming:
    def execute(self, module, input):
        global continue_dimming
        continue_dimming = False
        self.logger.info("Dimmen wird abgebrochen")
