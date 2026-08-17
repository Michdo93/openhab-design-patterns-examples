from openhab import rule, Registry
from openhab.triggers import GroupCommandTrigger


@rule(triggers=[GroupCommandTrigger("LightControls")])
class LightControlReceivedCommand:
    def execute(self, module, input):
        item_name = input["itemName"]
        command = input["command"]
        light_name, source = item_name.split("_")[0], item_name.split("_")[1]

        if source == "Proxy":
            return  # Proxy sollte nie direkt befehligt werden

        proxy = Registry.getItem(light_name + "_Proxy")
        device = Registry.getItem(light_name + "_Device")
        ui = Registry.getItem(light_name + "_UI")
        rules_item = Registry.getItem(light_name + "_Rules")

        if str(proxy.state) != str(command):
            proxy.postUpdate(command)
        if str(ui.state) != str(command):
            ui.postUpdate(command)
        if str(rules_item.state) != str(command):
            rules_item.postUpdate(command)
        if str(device.state) != str(command):
            device.sendCommand(command)
