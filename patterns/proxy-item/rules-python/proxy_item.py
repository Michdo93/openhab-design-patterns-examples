from openhab import rule, Registry
from openhab.triggers import ItemCommandTrigger, ItemStateUpdateTrigger


@rule(triggers=[ItemCommandTrigger("ProxySwitch")])
class ProxySwitchErhieltBefehl:
    def execute(self, module, input):
        event = input.get("event")
        if not event:
            return

        command = str(event.getItemCommand())
        bound = Registry.getItem("BoundSwitch")
        if str(bound.getState()) != command:
            bound.sendCommand(command)
            self.logger.info("ProxySwitch -> BoundSwitch: " + command)


@rule(triggers=[ItemStateUpdateTrigger("BoundSwitchUpdates")])
class BoundSwitchUpdatesErhieltUpdate:
    def execute(self, module, input):
        event = input.get("event")
        if not event:
            return

        state = str(event.getItemState())
        proxy = Registry.getItem("ProxySwitch")
        if str(proxy.getState()) != state:
            proxy.postUpdate(state)
            self.logger.info("BoundSwitchUpdates -> ProxySwitch: " + state)
