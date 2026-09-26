rules.JSRule({
  name: "Set lights based on Time of Day",
  triggers: [triggers.ItemStateChangeTrigger("vTimeOfDay")],
  execute: (event) => {
    const timeOfDay = items.getItem("vTimeOfDay").state;

    items.getItem("gLights").members.forEach((light) => {
      const setting = items.getItem("gSettings").members
        .find((s) => s.name === light.name + "_" + timeOfDay);
      if (!setting) {
        // Keine Einstellung für diese Tageszeit vorgesehen - kein Fehler
      } else if (setting.state === "NULL" || setting.state === "UNDEF") {
        console.warn(light.name + ": no setpoint set for " + timeOfDay + " yet");
      } else {
        light.sendCommand(String(setting.state));
        console.log(light.name + " -> " + setting.state);
      }
    });
  }
});
