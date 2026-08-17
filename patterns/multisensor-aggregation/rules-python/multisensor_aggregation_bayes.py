from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger

SENSOR_CONFIDENCE = {
    "MotionSensor": {"tp": 0.9, "fp": 0.1},
    "WindowSensor": {"tp": 0.8, "fp": 0.2},
    "LightSensor": {"tp": 0.7, "fp": 0.3},
}
PRIOR_PRESENCE = 0.5


@rule(triggers=[
    ItemStateChangeTrigger("MotionSensor"),
    ItemStateChangeTrigger("WindowSensor"),
    ItemStateChangeTrigger("LightSensor"),
])
class BayesianMultiSensorAggregation:
    def execute(self, module, input):
        states = {
            "MotionSensor": str(Registry.getItem("MotionSensor").state) == "ON",
            "WindowSensor": str(Registry.getItem("WindowSensor").state) == "CLOSED",
            "LightSensor": float(str(Registry.getItem("LightSensor").state)) > 100,
        }

        prob_presence = PRIOR_PRESENCE
        prob_absence = 1 - PRIOR_PRESENCE

        for sensor, detected in states.items():
            tp = SENSOR_CONFIDENCE[sensor]["tp"]
            fp = SENSOR_CONFIDENCE[sensor]["fp"]

            if detected:
                prob_presence *= tp
                prob_absence *= fp
            else:
                prob_presence *= (1 - tp)
                prob_absence *= (1 - fp)

        total = prob_presence + prob_absence
        prob_presence /= total

        self.logger.info("Bayes Anwesenheitswahrscheinlichkeit: {:.2f}".format(prob_presence))

        if prob_presence > 0.6:
            self.logger.info("Anwesenheit erkannt!")
        else:
            self.logger.info("Keine Anwesenheit.")
