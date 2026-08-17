from openhab import rule, Registry
from openhab.triggers import ItemCommandTrigger, ItemStateUpdateTrigger


@rule(triggers=[ItemCommandTrigger("ProxySwitch")])
class ProxySwitchErhieltBefehl:
    def execute(self, module, input):
        command = str(input["command"])
        bound = Registry.getItem("BoundSwitch")
        if str(bound.state) != command:
            bound.sendCommand(command)


@rule(triggers=[ItemStateUpdateTrigger("BoundSwitchUpdates")])
class BoundSwitchUpdatesErhieltUpdate:
    def execute(self, module, input):
        state = str(input["state"])
        proxy = Registry.getItem("ProxySwitch")
        if str(proxy.state) != state:
            proxy.postUpdate(state)
