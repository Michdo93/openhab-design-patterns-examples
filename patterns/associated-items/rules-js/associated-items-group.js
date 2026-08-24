const { rules, triggers, items } = require('openhab');

rules.JSRule({
  name: "Zugehoeriges Item ueber Gruppenzugehoerigkeit finden",
  triggers: [triggers.ItemGroupStateChangeTrigger("gSensors")], // Angepasst
  execute: (event) => {
    const sensors = items.getItem("gSensors").members; //[cite: 3]

    const status1 = sensors.find((i) => i.name === event.itemName + "_Status"); //[cite: 3]
    const status2 = sensors.find((i) => i.tags.includes("Status")); //[cite: 3]

    console.log("status1=" + (status1 && status1.name) + " status2=" + (status2 && status2.name)); //[cite: 3]
  }
});
