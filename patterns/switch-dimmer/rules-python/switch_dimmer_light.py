from openhab import rule, Registry
from openhab.triggers import ItemCommandTrigger

my_color_light_command = "INCREASE"


@rule(triggers=[ItemCommandTrigger("MySwitch1UpShortPress", "ON")])
class MyColorLightOnOff:
    def execute(self, module, input):
        global my_color_light_command
        hsb = str(Registry.getItem("MyColorLight").state)
        brightness = float(hsb.split(",")[2])
        if brightness == 0:
            my_color_light_command = "INCREASE"
            Registry.getItem("MyColorLight").sendCommand("ON")
        else:
            my_color_light_command = "DECREASE"
            Registry.getItem("MyColorLight").sendCommand("OFF")


@rule(triggers=[ItemCommandTrigger("MySwitch1UpLongPress", "ON")])
class MyColorLightDimmer:
    def execute(self, module, input):
        Registry.getItem("MyColorLight").sendCommand(my_color_light_command)
