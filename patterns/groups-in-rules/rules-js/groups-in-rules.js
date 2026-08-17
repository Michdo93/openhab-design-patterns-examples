rules.JSRule({
  name: "A Door Sensor Changed",
  triggers: [triggers.GroupStateChangeTrigger("gDoorsSensors")],
  execute: (event) => {
    const door = items.getItem(event.itemName);
    const timer = items.getItem(door.name + "_Timer");
    const lastUpdate = items.getItem(door.name + "_LastUpdate");

    if (door.state === "OPEN") timer.sendCommand("ON");
    else timer.postUpdate("OFF");

    lastUpdate.postUpdate(new Date().toISOString());

    let msg = door.name + (door.state === "OPEN" ? " was opened" : " was closed");

    let alert = false;
    const timeOfDay = items.getItem("vTimeOfDay").state;
    if (timeOfDay === "NIGHT" || timeOfDay === "BED") {
      alert = true;
      msg += " at night";
    }
    if (items.getItem("vPresent").state === "OFF") {
      alert = true;
      msg += " and no one is home";
    }

    if (alert) items.getItem("aAlerts").sendCommand(msg);
    console.log(msg);
  }
});

rules.JSRule({
  name: "Timer expired for a door",
  triggers: [triggers.GroupStateUpdateTrigger("gDoorsTimers", "OFF")],
  execute: (event) => {
    const doorName = event.itemName.split("_")[0];

    const openDoors = items.getItem("gDoorsSensors").members
      .filter((d) => d.state === "OPEN")
      .map((d) => d.name)
      .join(", ");

    let msg = doorName + " has been open for over an hour";
    if (openDoors) msg += " and also open: " + openDoors;

    items.getItem("aAlerts").sendCommand(msg);
    console.log(msg);

    const timeOfDay = items.getItem("vTimeOfDay").state;
    if (timeOfDay === "NIGHT" || timeOfDay === "BED") {
      items.getItem(event.itemName).sendCommand("ON");
    }
  }
});
