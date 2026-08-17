let ceilingTimer = null;

rules.JSRule({
  name: "Ceiling fan control",
  triggers: [triggers.ItemStateChangeTrigger("MotionSensor", undefined, "ON")],
  execute: (event) => {
    if (ceilingTimer !== null) return;

    const loop = () => {
      if (items.getItem("vTimeOfDay").state === "NIGHT") {
        let newState = "STAY";
        const current = parseFloat(items.getItem("CurrentTemp").state);
        const target = parseFloat(items.getItem("TargetTemp").state);
        if (current > target) newState = "ON";
        else if (current < target - 1) newState = "OFF";

        if (newState !== "STAY" && items.getItem("Fan").state !== newState) {
          items.getItem("Fan").sendCommand(newState);
        }

        ceilingTimer.reschedule(time.ZonedDateTime.now().plusSeconds(60));
      } else {
        ceilingTimer = null;
      }
    };

    ceilingTimer = actions.ScriptExecution.createTimer(time.ZonedDateTime.now(), loop);
  }
});
