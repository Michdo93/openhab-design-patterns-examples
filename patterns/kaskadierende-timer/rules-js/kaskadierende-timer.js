let irrigationTimer = null;

function itemExists(name) {
  try {
    return items.getItem(name) !== null;
  } catch (e) {
    return false;
  }
}

rules.JSRule({
  name: "Irrigation reset on system start",
  triggers: [triggers.SystemStartlevelTrigger(100)],
  execute: (event) => {
    items.getItem("gIrrigation").members.forEach((valve) => {
      if (valve.state !== "OFF") valve.sendCommand("OFF");
    });
    items.getItem("Irrigation_Curr").postUpdate("OFF");
  }
});

rules.JSRule({
  name: "Irrigation start at 08:00",
  triggers: [
    triggers.GenericCronTrigger("0 0 8 * * ?"),
    triggers.ItemCommandTrigger("Irrigation_Manual", "ON")
  ],
  execute: (event) => {
    if (items.getItem("Irrigation_Auto").state === "ON" || event.receivedCommand === "ON") {
      items.getItem("Irrigation_Manual").postUpdate("ON");
      console.log("Irrigation started, zone 1 active");
      items.getItem("Irrigation_Curr").sendCommand("Irrigation_Zone_1");
    }
  }
});

rules.JSRule({
  name: "Irrigation Cascade",
  triggers: [triggers.ItemCommandTrigger("Irrigation_Curr")],
  execute: (event) => {
    const currValveName = event.receivedCommand;
    const currValve = items.getItem(currValveName);
    const currValveNum = parseInt(currValveName.split("_")[2]);
    const timeState = items.getItem(currValveName + "_Time").state;
    if (timeState === "NULL" || timeState === "UNDEF") {
      console.warn("No time set for " + currValveName);
      return;
    }
    const currValveMins = parseInt(timeState);
    const nextValveName = "Irrigation_Zone_" + (currValveNum + 1);

    currValve.sendCommand("ON");

    irrigationTimer = actions.ScriptExecution.createTimer(
      time.ZonedDateTime.now().plusMinutes(currValveMins),
      () => {
        console.log("Zone " + currValveName + " off");
        currValve.sendCommand("OFF");

        if (itemExists(nextValveName)) {
          console.log("Zone " + nextValveName + " on");
          items.getItem("Irrigation_Curr").sendCommand(nextValveName);
        } else {
          console.log("Irrigation finished");
          items.getItem("Irrigation_Manual").sendCommand("OFF");
        }
        irrigationTimer = null;
      }
    );
  }
});

rules.JSRule({
  name: "Irrigation Cancel",
  triggers: [triggers.ItemCommandTrigger("Irrigation_Manual", "OFF")],
  execute: (event) => {
    if (irrigationTimer !== null) {
      irrigationTimer.cancel();
      irrigationTimer = null;
    }
    items.getItem("gIrrigation").members.forEach((valve) => {
      if (valve.state !== "OFF") valve.sendCommand("OFF");
    });
    items.getItem("Irrigation_Curr").postUpdate("OFF");
  }
});
