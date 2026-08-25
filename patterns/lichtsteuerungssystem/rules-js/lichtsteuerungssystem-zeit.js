rules.JSRule({
  name: "Adjust light levels based on time",
  triggers: [triggers.GenericCronTrigger("0 30 6 ? * * *")],
  execute: (event) => {
    items.getItem("PresetDimLevel").postUpdate(20);
    items.getItem("UpdateLightLevels").sendCommand("ON");
    console.log("PresetDimLevel -> 20, UpdateLightLevels -> ON");
  }
});
