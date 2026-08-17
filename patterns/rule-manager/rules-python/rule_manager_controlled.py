from openhab import rule, Registry


@rule(triggers=[])  # Trigger der Beispielregel
class ExampleRule:
    def execute(self, module, input):
        Registry.getItem("isRunningExampleRule").sendCommand("ON")

        if str(Registry.getItem("isRunningExampleRule").state) == "ON":
            pass  # Teil 1 der Regel
        else:
            pass  # Aenderungen rueckgaengig machen

        if str(Registry.getItem("isRunningExampleRule").state) == "ON":
            pass  # Teil 2 der Regel
        else:
            pass  # Aenderungen rueckgaengig machen

        Registry.getItem("isRunningExampleRule").sendCommand("OFF")
