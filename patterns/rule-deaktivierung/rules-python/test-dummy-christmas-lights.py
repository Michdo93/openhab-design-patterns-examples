# Reine Test-Hilfsdatei, um "rule_deaktivierung.py" testen zu koennen -
# im echten Einsatz waeren das eure tatsaechlichen Weihnachtslicht-Regeln.
from openhab import rule

@rule(uid="christmas_lights", name="Christmas Lights (Test-Dummy)", triggers=[])
class ChristmasLightsDummy:
    def execute(self, module, input):
        pass
