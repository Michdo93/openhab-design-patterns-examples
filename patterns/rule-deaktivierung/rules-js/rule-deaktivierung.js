rules.JSRule({
  name: "Christmas Mode",
  description: "Enable/disable rules based on the state of vChristmas",
  tags: ["christmas"],
  triggers: [
    triggers.ItemStateChangeTrigger("vChristmas"),
    triggers.SystemStartlevelTrigger(100)
  ],
  execute: (event) => {
    const christmasOn = items.getItem("vChristmas").state === "ON";

    rules.setEnabled("christmas_lights", christmasOn);
    rules.setEnabled("mbr_humidifier", !christmasOn);
  }
});
