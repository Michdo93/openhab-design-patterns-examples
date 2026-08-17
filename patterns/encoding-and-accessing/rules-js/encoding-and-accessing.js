const presentTargets = {
  "Room1_Thermostat": 21,
  "Room2_Thermostat": 22
};
const awayTargets = {
  "Room1_Thermostat": 17,
  "Room2_Thermostat": 18
};

rules.JSRule({
  name: "Zieltemperaturen anwenden",
  triggers: [triggers.ItemStateChangeTrigger("vPresent")],
  execute: (event) => {
    const targets = items.getItem("vPresent").state === "ON" ? presentTargets : awayTargets;
    Object.entries(targets).forEach(([name, temp]) => {
      items.getItem(name).sendCommand(temp);
    });
  }
});
