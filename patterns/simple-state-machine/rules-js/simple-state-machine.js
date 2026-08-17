rules.JSRule({
  name: "TimeOfDay MORNING (nur Wochentage)",
  triggers: [triggers.GenericCronTrigger("0 0 6 * * ?")],
  execute: (event) => {
    if (actions.Ephemeris.isWeekday()) {
      items.getItem("TimeOfDay").sendCommand("MORNING");
    }
  }
});
