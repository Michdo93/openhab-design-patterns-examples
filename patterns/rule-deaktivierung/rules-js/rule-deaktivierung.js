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

    try {
      rules.setEnabled("christmas_lights", christmasOn);
      rules.setEnabled("mbr_humidifier", !christmasOn);
      console.log("vChristmas=" + christmasOn + " -> christmas_lights enabled=" + christmasOn + ", mbr_humidifier enabled=" + !christmasOn);
    } catch (e) {
      console.warn("Konnte Regeln noch nicht umschalten (evtl. beim Start, Dummy-Regeln noch nicht geladen): " + e.message);
    }
  }
});
