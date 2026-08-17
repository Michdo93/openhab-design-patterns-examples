let occupancyTimer = null;

rules.JSRule({
  name: "MotionDetector1 received ON",
  triggers: [triggers.ItemStateUpdateTrigger("MotionDetector1", "ON")],
  execute: (event) => {
    if (occupancyTimer === null || occupancyTimer.hasTerminated()) {
      occupancyTimer = actions.ScriptExecution.createTimer(
        time.ZonedDateTime.now().plusMinutes(5),
        () => {
          items.getItem("MotionDetector1").sendCommand("OFF");
          occupancyTimer = null;
        }
      );
    } else {
      occupancyTimer.reschedule(time.ZonedDateTime.now().plusMinutes(5));
    }
  }
});
