# Reine Test-Hilfsdatei, um "rule_deaktivierung.py" testen zu koennen -
# im echten Einsatz waeren das eure tatsaechlichen Weihnachtslicht-Regeln.
from openhab import rule
from openhab.triggers import ItemCommandTrigger


@rule(uid="christmas_lights", name="Christmas Lights (Test-Dummy)",
      triggers=[ItemCommandTrigger("DummyRuleTrigger")])
class ChristmasLightsDummy:
    def execute(self, module, input):
        pass
