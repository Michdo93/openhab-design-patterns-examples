rules.JSRule({
  name: "Garage Lights Commanded On",
  triggers: [triggers.ItemStateChangeTrigger("GarageLightsProxy", undefined, "ON")],
  execute: (event) => { items.getItem("GLSM").postUpdate(GLSM_ON); }
});

rules.JSRule({
  name: "Garage Lights Commanded Off",
  triggers: [triggers.ItemStateChangeTrigger("GarageLightsProxy", undefined, "OFF")],
  execute: (event) => { items.getItem("GLSM").postUpdate(GLSM_OFF); }
});
