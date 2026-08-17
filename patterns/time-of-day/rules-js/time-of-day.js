const TimesOfDay = {
  week: [
    ["MORNING",   "07:05", "12:00"],
    ["AFTERNOON", "12:00", "19:00"],
    ["EVENING",   "19:00", "23:00"],
    ["NIGHT",     "23:00", "24:00"]
  ],
  saturday: [
    ["MORNING",   "08:00", "12:00"],
    ["AFTERNOON", "12:00", "19:00"],
    ["EVENING",   "19:00", "23:30"],
    ["NIGHT",     "23:30", "24:00"]
  ],
  sunday: [
    ["MORNING",   "08:30", "12:00"],
    ["AFTERNOON", "12:00", "18:00"],
    ["EVENING",   "18:00", "22:30"],
    ["NIGHT",     "22:30", "24:00"]
  ]
};

function minOfDay(s) {
  const hour = parseInt(s.slice(0, 2));
  const minute = parseInt(s.slice(3, 5));
  return hour * 60 + minute;
}

rules.JSRule({
  name: "Set vTimeOfDay",
  triggers: [
    triggers.SystemStartlevelTrigger(100),
    triggers.GenericCronTrigger("0 * * * * ?")
  ],
  execute: (event) => {
    const now = new Date();
    const nowMOD = now.getHours() * 60 + now.getMinutes();
    const weekday = now.getDay();
    const table = weekday === 0 ? TimesOfDay.sunday
                : weekday === 6 ? TimesOfDay.saturday
                : TimesOfDay.week;

    const prev = items.getItem("vTimeOfDay").state;
    let curr = "UNKNOWN";

    for (const [state, startStr, endStr] of table) {
      const start = minOfDay(startStr);
      const end = minOfDay(endStr);
      if (nowMOD >= start && nowMOD < end) {
        curr = state;
        break;
      }
    }

    if (curr !== prev) {
      items.getItem("vTimeOfDay").sendCommand(curr);
      console.log("vTimeOfDay -> " + curr);
    }
  }
});
