const timers = new Map();
const TIMEOUT_MINUTES = 5;

rules.JSRule({
  name: "A Motion Detector triggered",
  triggers: [triggers.GroupCommandTrigger("gMotionDetectors", "ON")],
  execute: (event) => {
    const triggeringItem = items.getItem(event.itemName);
    const existing = timers.get(triggeringItem.name);

    if (!existing || existing.hasTerminated()) {
      console.log(triggeringItem.name + ": Timer gestartet (" + TIMEOUT_MINUTES * 60 + "s)");
      const t = actions.ScriptExecution.createTimer(
        time.ZonedDateTime.now().plusMinutes(TIMEOUT_MINUTES),
        () => {
          triggeringItem.sendCommand("OFF");
          timers.delete(triggeringItem.name);
        }
      );
      timers.set(triggeringItem.name, t);
    } else {
      existing.reschedule(time.ZonedDateTime.now().plusMinutes(TIMEOUT_MINUTES));
    }
  }
});
