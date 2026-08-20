from openhab import rule, Registry
from openhab.triggers import ItemCommandTrigger

STAIRS_PREFIXES = ("FEDL", "F1DL", "F2WL")


def set_stairs_dim(value):
    for prefix in STAIRS_PREFIXES:
        Registry.getItem(prefix + "_DIMM").sendCommand(value)
        Registry.getItem(prefix + "_TOGGLE").sendCommand("ON")


def switch_off_stairs():
    for prefix in STAIRS_PREFIXES:
        Registry.getItem(prefix + "_TOGGLE").sendCommand("OFF")


SCENES = {
    "SwitchOff_LightsStairs": switch_off_stairs,
    "SwitchOn_LightsStairs025": lambda: set_stairs_dim(25),
    "SwitchOn_LightsStairs050": lambda: set_stairs_dim(50),
    "SwitchOn_LightsStairs075": lambda: set_stairs_dim(75),
    "SwitchOn_LightsStairs100": lambda: set_stairs_dim(100),
}


@rule(triggers=[ItemCommandTrigger("callScriptItem")])
class CallScene:
    def execute(self, module, input):
        event = input.get("event")
        if not event:
            return

        scene_name = str(event.getItemCommand())
        self.logger.info("scene: " + scene_name)
        scene = SCENES.get(scene_name)
        if scene:
            scene()
        else:
            self.logger.warn("Unbekannte Szene: " + scene_name)
