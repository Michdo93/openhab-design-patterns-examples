rules.JSRule({
  name: "Motion detected",
  triggers: [triggers.ItemStateUpdateTrigger("MotionSensor1", "ON")],
  execute: (event) => {
    if (items.getItem("Light1").state === "OFF") {
      items.getItem("Light1").sendCommand("ON");
      console.log("Motion detected - Light1 switched on (10 min timer)");
      actions.ScriptExecution.createTimer(time.ZonedDateTime.now().plusMinutes(10), () => {
        items.getItem("Light1").sendCommand("OFF");
      });
    } else {
      console.log("Motion detected, but Light1 was already on");
    }
  }
});
