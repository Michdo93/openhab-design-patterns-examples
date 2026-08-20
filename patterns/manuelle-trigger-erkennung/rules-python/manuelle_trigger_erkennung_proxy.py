from openhab import rule, Registry
from openhab.triggers import GroupCommandTrigger


@rule(triggers=[GroupCommandTrigger("LightControls")])
class LightControlReceivedCommand:
    def execute(self, module, input):
        event = input.get("event")
        if not event:
            return

        item_name = event.getItemName()
        command = str(event.getItemCommand())
        light_name, source = item_name.split("_")[0], item_name.split("_")[1]

        if source == "Proxy":
            return  # Proxy sollte nie direkt befehligt werden

        proxy = Registry.getItem(light_name + "_Proxy")
        device = Registry.getItem(light_name + "_Device")
        ui = Registry.getItem(light_name + "_UI")
        rules_item = Registry.getItem(light_name + "_Rules")

        if str(proxy.getState()) != command:
            proxy.postUpdate(command)
        if str(ui.getState()) != command:
            ui.postUpdate(command)
        if str(rules_item.getState()) != command:
            rules_item.postUpdate(command)
        if str(device.getState()) != command:
            device.sendCommand(command)

        self.logger.info("Quelle=" + source + " -> " + light_name + " = " + command)
