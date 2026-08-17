from openhab import rule, Registry
from openhab.triggers import ItemStateChangeTrigger

PRIOR = 0.5
THRESHOLD = 0.85


def update_probability(prior, prob_given_true, prob_given_false):
    numerator = prob_given_true * prior
    return numerator / (numerator + prob_given_false * (1 - prior))


@rule(triggers=[
    ItemStateChangeTrigger("myObservation1"),
    ItemStateChangeTrigger("myObservation2"),
    ItemStateChangeTrigger("myObservation3"),
    ItemStateChangeTrigger("myObservation4"),
])
class BayesianSleepSensor:
    def execute(self, module, input):
        prob = PRIOR

        if str(Registry.getItem("myObservation1").state) == "OFF":
            prob = update_probability(prob, 0.99, 0.5)
        if str(Registry.getItem("myObservation2").state) == "NIGHT":
            prob = update_probability(prob, 0.75, 0.3)
        if str(Registry.getItem("myObservation3").state) == "OFF":
            prob = update_probability(prob, 0.9, 0.4)
        if str(Registry.getItem("myObservation4").state) == "ON":
            prob = update_probability(prob, 0.95, 0.5)

        Registry.getItem("mySleepProbability").postUpdate(prob * 100)
        Registry.getItem("mySleepSensor").sendCommand("ON" if prob >= THRESHOLD else "OFF")
