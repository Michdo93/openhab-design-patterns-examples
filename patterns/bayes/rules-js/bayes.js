const PRIOR = 0.5;
const THRESHOLD = 0.85;

function updateProbability(prior, probGivenTrue, probGivenFalse) {
  const numerator = probGivenTrue * prior;
  return numerator / (numerator + probGivenFalse * (1 - prior));
}

rules.JSRule({
  name: "Bayesian Sleep Sensor",
  triggers: [
    triggers.ItemStateChangeTrigger("myObservation1"),
    triggers.ItemStateChangeTrigger("myObservation2"),
    triggers.ItemStateChangeTrigger("myObservation3"),
    triggers.ItemStateChangeTrigger("myObservation4")
  ],
  execute: (event) => {
    let prob = PRIOR;

    if (items.getItem("myObservation1").state === "OFF") prob = updateProbability(prob, 0.99, 0.5);
    if (items.getItem("myObservation2").state === "NIGHT") prob = updateProbability(prob, 0.75, 0.3);
    if (items.getItem("myObservation3").state === "OFF") prob = updateProbability(prob, 0.9, 0.4);
    if (items.getItem("myObservation4").state === "ON") prob = updateProbability(prob, 0.95, 0.5);

    items.getItem("mySleepProbability").postUpdate(prob * 100);
    items.getItem("mySleepSensor").sendCommand(prob >= THRESHOLD ? "ON" : "OFF");
  }
});
