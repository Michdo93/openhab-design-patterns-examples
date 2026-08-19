from openhab import rule, Registry
from openhab.triggers import ItemCommandTrigger


@rule(triggers=[ItemCommandTrigger("myCounter")])
class CountdownVerwaltung:
    def execute(self, module, input):
        event = input.get("event")
        if not event:
            return

        cmmd = int(str(event.getItemCommand()))
        count = 0
        state = Registry.getItem("myCounter").getState()
        if str(state) != "NULL":
            count = int(str(state))

        if cmmd == -1 and count > 0:
            if count == 1:
                Registry.getItem("testLamp").sendCommand("OFF")
            Registry.getItem("myCounter").postUpdate(count - 1)
        elif cmmd >= count or cmmd < -1:
            new_count = -cmmd if cmmd < -1 else cmmd
            Registry.getItem("myCounter").postUpdate(new_count)
            if str(Registry.getItem("testLamp").getState()) != "ON":
                Registry.getItem("testLamp").sendCommand("ON")
        elif cmmd == 0:
            Registry.getItem("myCounter").postUpdate(0)
            Registry.getItem("testLamp").sendCommand("OFF")


@rule(triggers=[ItemCommandTrigger("test6")])
class SechsMinutenStarten:
    def execute(self, module, input):
        Registry.getItem("myCounter").sendCommand(6)


@rule(triggers=[ItemCommandTrigger("test3")])
class DreiMinutenStarten:
    def execute(self, module, input):
        Registry.getItem("myCounter").sendCommand(3)


@rule(triggers=[ItemCommandTrigger("test2")])
class AufZweiMinutenSetzen:
    def execute(self, module, input):
        Registry.getItem("myCounter").sendCommand(-2)


@rule(triggers=[ItemCommandTrigger("testabort")])
class CountdownAbbrechen:
    def execute(self, module, input):
        Registry.getItem("myCounter").sendCommand(0)
