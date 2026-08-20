rules.JSRule({
  name: "Set lights based on Time of Day",
  triggers: [triggers.ItemStateChangeTrigger("vTimeOfDay")],
  execute: (event) => {
    const timeOfDay = items.getItem("vTimeOfDay").state;

    items.getItem("gLights").members.forEach((light) => {
      const setting = items.getItem("gSettings").members
        .find((s) => s.name === light.name + "_" + timeOfDay);
      if (setting && setting.state !== "NULL" && setting.state !== "UNDEF") {
        light.sendCommand(String(setting.state));
      }
    });
  }
});
