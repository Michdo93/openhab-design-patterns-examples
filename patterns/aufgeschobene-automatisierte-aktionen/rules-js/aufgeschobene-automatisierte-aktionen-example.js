rules.JSRule({
  name: "Open blinds after sunrise",
  triggers: [triggers.ItemStateChangeTrigger("DayNight", "NIGHT", "DAY")],
  execute: (event) => {
    items.getItem("LoungeBlind_Timer").sendCommand("+15m->UP");
  }
});
