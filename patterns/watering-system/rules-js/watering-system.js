const wateringTimers = new Map();

rules.JSRule({
  name: "Watering Service",
  triggers: [
    triggers.ItemStateChangeTrigger("VT_Watering_Zone1"),
    triggers.ItemStateChangeTrigger("VT_Watering_Zone2")
  ],
  execute: (event) => {
    const zone = event.itemName;
    const duration = parseInt(items.getItem("VT_Watering_Duration").state);
    const relayName = zone.replace("VT_Watering_", "") + "_Relay";

    if (items.getItem(zone).state === "START") {
      console.log("Starte Bewaesserung fuer Zone " + zone + " fuer " + duration + " Sekunden");
      items.getItem(relayName).sendCommand("ON");

      const t = actions.ScriptExecution.createTimer(
        time.ZonedDateTime.now().plusSeconds(duration),
        () => {
          console.log("Beende Bewaesserung fuer Zone " + zone);
          items.getItem(relayName).sendCommand("OFF");
          wateringTimers.delete(zone);
        }
      );
      wateringTimers.set(zone, t);
    }
  }
});
