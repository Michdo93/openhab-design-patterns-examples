# Reine Test-Hilfsdatei, um "rule_deaktivierung.py" testen zu können -
# im echten Einsatz wäre das eure tatsächliche Luftbefeuchter-Regel.
from openhab import rule
from openhab.triggers import ItemCommandTrigger


@rule(uid="mbr_humidifier", name="MBR Humidifier (Test-Dummy)",
      triggers=[ItemCommandTrigger("DummyRuleTrigger")])
class MbrHumidifierDummy:
    def execute(self, module, input):
        pass
