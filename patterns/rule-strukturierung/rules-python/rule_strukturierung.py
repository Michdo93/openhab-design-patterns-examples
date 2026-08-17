from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger


@rule(triggers=[
    ItemStateChangeTrigger("Foo"),
    ItemStateChangeTrigger("Bar"),
    ItemStateChangeTrigger("Baz"),
])
class OneToTwoThreeRuleStructure:
    def execute(self, module, input):
        foo = str(Registry.getItem("Foo").state)
        bar = str(Registry.getItem("Bar").state)
        baz = str(Registry.getItem("Baz").state)

        # 1. Pruefen, ob Regel laufen muss
        if "NULL" in (foo, bar, baz):
            self.logger.warn("One of the Items is NULL")
            return

        # 2. Berechnen
        on_count = [foo, bar, baz].count("ON")
        new_state = "ON" if on_count >= 2 else "OFF"

        # 3. Ausfuehren
        Registry.getItem("Buzz").sendCommand(new_state)
