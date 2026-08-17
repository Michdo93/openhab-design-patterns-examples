rules.JSRule({
  name: "Set lights based on Time of Day",
  triggers: [triggers.ItemStateChangeTrigger("vTimeOfDay")],
  execute: (event) => {
    items.getItem("gLights_WEATHER_OVERRIDE").postUpdate("OFF");

    const timeOfDay = items.getItem("vTimeOfDay").state;

    const offGroup = items.getItem("gLights_OFF").members.find((g) => g.name === "gLights_OFF_" + timeOfDay);
    if (offGroup) {
      offGroup.members.filter((l) => l.state !== "OFF").forEach((l) => l.sendCommand("OFF"));
    }

    const onGroup = items.getItem("gLights_ON").members.find((g) => g.name === "gLights_ON_" + timeOfDay);
    if (onGroup) {
      onGroup.members.filter((l) => l.state !== "ON").forEach((l) => l.sendCommand("ON"));
    }
  }
});
