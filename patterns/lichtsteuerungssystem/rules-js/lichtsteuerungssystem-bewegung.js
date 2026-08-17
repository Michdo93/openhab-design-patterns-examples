rules.JSRule({
  name: "Motion detected",
  triggers: [triggers.ItemStateUpdateTrigger("MotionSensor1", "ON")],
  execute: (event) => {
    if (items.getItem("Light1").state === "OFF") {
      items.getItem("Light1").sendCommand("ON");
      actions.ScriptExecution.createTimer(time.ZonedDateTime.now().plusMinutes(10), () => {
        items.getItem("Light1").sendCommand("OFF");
      });
    }
  }
});
