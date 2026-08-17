from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger


@rule(triggers=[
    ItemStateChangeTrigger("MotionSensor"),
    ItemStateChangeTrigger("WindowSensor"),
    ItemStateChangeTrigger("LightSensor"),
])
class MultiSensorConfidenceAggregation:
    def execute(self, module, input):
        motion_conf = 0.7 if str(Registry.getItem("MotionSensor").state) == "ON" else 0.0
        window_conf = 0.5 if str(Registry.getItem("WindowSensor").state) == "CLOSED" else 0.0
        light_conf = 0.3 if float(str(Registry.getItem("LightSensor").state)) > 100 else 0.0

        aggregated_conf = motion_conf + window_conf + light_conf

        self.logger.info("Aggregierte Konfidenz: {}".format(aggregated_conf))

        if aggregated_conf > 0.6:
            self.logger.info("Anwesenheit erkannt!")
            # Registry.getItem("LightSwitch").sendCommand("ON")
        else:
            self.logger.info("Keine Anwesenheit.")
