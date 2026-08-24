rules.JSRule({
  name: "Zugehoeriges Item ueber Gruppenzugehoerigkeit finden",
  triggers: [triggers.ItemStateChangeTrigger("gSensors")],
  execute: (event) => {
    const sensors = items.getItem("gSensors").members;
    const status1 = sensors.find((i) => i.name === event.itemName + "_Status");
    const status2 = sensors.find((i) => i.tags.includes("Status"));

    console.log("status1=" + (status1 && status1.name) + " status2=" + (status2 && status2.name));
  }
});
