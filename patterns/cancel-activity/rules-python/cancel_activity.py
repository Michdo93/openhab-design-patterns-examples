import threading

from openhab import rule, Registry
from openhab.triggers import ItemCommandTrigger

dim_timer = None
continue_dimming = True


def step():
    global dim_timer, continue_dimming
    curr_level = int(str(Registry.getItem("DimLamp").state))
    target = int(str(Registry.getItem("DimTarget").state))

    if curr_level >= target or not continue_dimming:
        print("Dimmen beendet")
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
        step()


@rule(triggers=[ItemCommandTrigger("CancelDimTrigger", "ON")])
class CancelDimming:
    def execute(self, module, input):
        global continue_dimming
        continue_dimming = False
