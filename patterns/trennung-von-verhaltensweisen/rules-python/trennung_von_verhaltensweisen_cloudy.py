from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger


@rule(triggers=[ItemStateChangeTrigger("vCloudiness")])
class IsItCloudyOutside:
    def execute(self, module, input):
        cloudiness = float(str(Registry.getItem("vCloudiness").state))
        new_state = "ON" if cloudiness > 50 else "OFF"

        is_cloudy = Registry.getItem("vIsCloudy")
        if new_state != str(is_cloudy.state):
            is_cloudy.postUpdate(new_state)
