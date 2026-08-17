const SENSOR_CONFIDENCE = {
  MotionSensor: { tp: 0.9, fp: 0.1 },
  WindowSensor: { tp: 0.8, fp: 0.2 },
  LightSensor: { tp: 0.7, fp: 0.3 }
};
const PRIOR_PRESENCE = 0.5;

rules.JSRule({
  name: "Bayesian Multi-Sensor Aggregation",
  triggers: [
    triggers.ItemStateChangeTrigger("MotionSensor"),
    triggers.ItemStateChangeTrigger("WindowSensor"),
    triggers.ItemStateChangeTrigger("LightSensor")
  ],
  execute: (event) => {
    const states = {
      MotionSensor: items.getItem("MotionSensor").state === "ON",
      WindowSensor: items.getItem("WindowSensor").state === "CLOSED",
      LightSensor: parseFloat(items.getItem("LightSensor").state) > 100
    };

    let probPresence = PRIOR_PRESENCE;
    let probAbsence = 1 - PRIOR_PRESENCE;

    Object.entries(states).forEach(([sensor, detected]) => {
      const { tp, fp } = SENSOR_CONFIDENCE[sensor];
      if (detected) {
        probPresence *= tp;
        probAbsence *= fp;
      } else {
        probPresence *= (1 - tp);
        probAbsence *= (1 - fp);
      }
    });

    const total = probPresence + probAbsence;
    probPresence /= total;

    console.log("Bayes Anwesenheitswahrscheinlichkeit: " + probPresence.toFixed(2));

    if (probPresence > 0.6) {
      console.log("Anwesenheit erkannt!");
    } else {
      console.log("Keine Anwesenheit.");
    }
  }
});
