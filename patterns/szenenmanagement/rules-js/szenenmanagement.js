const scenes = {
  "SwitchOff_LightsStairs": () => {
    ["FEDL", "F1DL", "F2WL"].forEach((prefix) => {
      items.getItem(prefix + "_TOGGLE").sendCommand("OFF");
    });
  },
  "SwitchOn_LightsStairs025": () => setStairsDim(25),
  "SwitchOn_LightsStairs050": () => setStairsDim(50),
  "SwitchOn_LightsStairs075": () => setStairsDim(75),
  "SwitchOn_LightsStairs100": () => setStairsDim(100)
};

function setStairsDim(value) {
  ["FEDL", "F1DL", "F2WL"].forEach((prefix) => {
    items.getItem(prefix + "_DIMM").sendCommand(value);
    items.getItem(prefix + "_TOGGLE").sendCommand("ON");
  });
}

rules.JSRule({
  name: "call scene",
  triggers: [triggers.ItemCommandTrigger("callScriptItem")],
  execute: (event) => {
    const sceneName = event.receivedCommand;
    console.log("scene: " + sceneName);
    const scene = scenes[sceneName];
    if (scene) scene();
    else console.warn("Unbekannte Szene: " + sceneName);
  }
});
