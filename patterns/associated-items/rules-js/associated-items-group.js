rules.JSRule({
  name: "Zugehoeriges Item ueber Gruppenzugehoerigkeit finden",
  triggers: [triggers.GroupStateChangeTrigger("gSensors")],
  execute: (event) => {
    const sensors = items.getItem("gSensors").members;

    // Ansatz: Item-Name
    const status1 = sensors.find((i) => i.name === event.itemName + "_Status");

    // Ansatz: Item-Tag
    const status2 = sensors.find((i) => i.tags.includes("Status"));

    // Ansatz: Item-Tags
    const status3 = sensors.find(
      (i) => ["Status", "Power"].every((tag) => i.tags.includes(tag))
    );

    // Ansatz: mehrere Kriterien
    const status4 = sensors.find(
      (i) => i.tags.includes("Status") && i.name.endsWith("_Status") && i.type === "Switch"
    );

    console.log("status1=" + (status1 && status1.name) + " status2=" + (status2 && status2.name));
  }
});
