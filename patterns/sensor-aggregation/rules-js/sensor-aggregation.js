rules.JSRule({
  name: "Reset vPresent to OFF on startup",
  triggers: [triggers.SystemStartlevelTrigger(100)],
  execute: (event) => {
    items.getItem("vPresent").sendCommand("OFF");
    items.getItem("gPresent").members.forEach((s) => s.sendCommand("OFF"));
  }
});

rules.JSRule({
  name: "A presence sensor updated",
  triggers: [triggers.GroupStateChangeTrigger("gPresent")],
  execute: (event) => {
    const count = parseFloat(items.getItem("gPresent").state);
    const vPresent = items.getItem("vPresent");
    const tPresent = items.getItem("tPresent");

    console.debug("gPresent changed to " + count);
    if (count > 0 && (vPresent.state !== "ON" || tPresent.state === "ON")) {
      console.debug("Someone came home");
      if (tPresent.state !== "OFF") tPresent.postUpdate("OFF");
      if (vPresent.state !== "ON") vPresent.sendCommand("ON");
    } else if (count === 0 && vPresent.state !== "OFF" && tPresent.state !== "ON") {
      console.debug("Everyone is away, setting timer");
      tPresent.sendCommand("ON");
    }
  }
});

rules.JSRule({
  name: "Present timer expired, no one is home",
  triggers: [triggers.ItemCommandTrigger("tPresent", "OFF")],
  execute: (event) => {
    const count = parseFloat(items.getItem("gPresent").state);
    if (count === 0) {
      console.log("Everyone is away, setting house to away");
      items.getItem("vPresent").sendCommand("OFF");
    } else {
      console.warn("Presence Timer expired but gPresent is " + count);
    }
  }
});
