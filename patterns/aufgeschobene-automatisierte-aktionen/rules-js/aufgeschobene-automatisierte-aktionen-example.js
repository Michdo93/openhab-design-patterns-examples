rules.JSRule({
  name: "Rollladen nach Sonnenaufgang öffnen",
  triggers: [triggers.ItemStateChangeTrigger("DayNight", "NIGHT", "DAY")],
  execute: (event) => {
    items.getItem("LoungeBlind_Timer").sendCommand("+15m->UP");
  }
});
