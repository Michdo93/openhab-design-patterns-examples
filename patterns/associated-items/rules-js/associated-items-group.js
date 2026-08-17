// Ansatz: Item-Name
const status1 = items.getItem("gSensors").members.find((i) => i.name === event.itemName + "_Status");

// Ansatz: Item-Tag
const status2 = items.getItem("gSensors").members.find((i) => i.tags.includes("Status"));

// Ansatz: Item-Tags
const status3 = items.getItem("gSensors").members.find(
  (i) => ["Status", "Power"].every((tag) => i.tags.includes(tag))
);

// Ansatz: mehrere Kriterien
const status4 = items.getItem("gSensors").members.find(
  (i) => i.tags.includes("Status") && i.name.endsWith("_Status") && i.type === "Switch"
);
