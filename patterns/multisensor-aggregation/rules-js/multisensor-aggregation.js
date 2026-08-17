rules.JSRule({
  name: "Multi-Sensor Confidence Aggregation",
  triggers: [
    triggers.ItemStateChangeTrigger("MotionSensor"),
    triggers.ItemStateChangeTrigger("WindowSensor"),
    triggers.ItemStateChangeTrigger("LightSensor")
  ],
  execute: (event) => {
    const motionConfidence = items.getItem("MotionSensor").state === "ON" ? 0.7 : 0.0;
    const windowConfidence = items.getItem("WindowSensor").state === "CLOSED" ? 0.5 : 0.0;
    const lightConfidence = parseFloat(items.getItem("LightSensor").state) > 100 ? 0.3 : 0.0;

    const aggregatedConfidence = motionConfidence + windowConfidence + lightConfidence;

    console.log("Aggregierte Konfidenz: " + aggregatedConfidence);

    if (aggregatedConfidence > 0.6) {
      console.log("Anwesenheit erkannt!");
      // items.getItem("LightSwitch").sendCommand("ON");
    } else {
      console.log("Keine Anwesenheit.");
    }
  }
});
