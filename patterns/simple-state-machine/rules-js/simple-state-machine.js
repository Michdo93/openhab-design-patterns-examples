rules.JSRule({
  name: "TimeOfDay MORNING (weekdays only)",
  triggers: [triggers.GenericCronTrigger("0 0 6 * * ?")],
  execute: (event) => {
    if (actions.Ephemeris.isWeekday()) {
      items.getItem("TimeOfDay").sendCommand("MORNING");
    }
  }
});
