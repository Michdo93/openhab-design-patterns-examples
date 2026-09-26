rules.JSRule({
  name: "Conditional Sequence Trigger",
  triggers: [triggers.GroupStateChangeTrigger("gCST")],
  execute: (event) => {
    const hour = time.ZonedDateTime.now().hour();
    const motionOn = items.getItem("motionSensor").state === "ON";
    const presenceOn = items.getItem("presenceSensor").state === "ON";

    if (motionOn && presenceOn && hour >= 18 && hour <= 22) {
      console.log("All conditions met - starting sequence");
      items.getItem("light").sendCommand("ON");
      // Weitere Aktionen in definierter Reihenfolge
    } else {
      console.log("Conditions not met - resetting sequence");
      items.getItem("light").sendCommand("OFF");
      // optional: alle Zwischenschritte abbrechen
    }
  }
});
