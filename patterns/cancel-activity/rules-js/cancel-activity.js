let dimTimer = null;
let continueDimming = true;

rules.JSRule({
  name: "Start Dimming",
  triggers: [triggers.ItemCommandTrigger("StartDimTrigger", "ON")],
  execute: (event) => {
    continueDimming = true;

    function step() {
      const currLevel = isNaN(parseInt(items.getItem("DimLamp").state)) ? 0 : parseInt(items.getItem("DimLamp").state);
      const target = isNaN(parseInt(items.getItem("DimTarget").state)) ? 0 : parseInt(items.getItem("DimTarget").state);

      if (currLevel >= target || !continueDimming) {
        console.log("Dimmen beendet");
        dimTimer = null;
        return;
      }

      items.getItem("DimLamp").sendCommand(currLevel + 1);
      dimTimer.reschedule(time.ZonedDateTime.now().plusSeconds(1));
    }

    dimTimer = actions.ScriptExecution.createTimer(time.ZonedDateTime.now(), step);
  }
});

rules.JSRule({
  name: "Cancel Dimming",
  triggers: [triggers.ItemCommandTrigger("CancelDimTrigger", "ON")],
  execute: (event) => {
    continueDimming = false;
  }
});
