const GLSM_OFF = "0";
const GLSM_ON = "1";

rules.JSRule({
  name: "Garage Lights Commanded On",
  triggers: [triggers.ItemStateChangeTrigger("GarageLightsProxy", undefined, "ON")],
  execute: (event) => {
    items.getItem("GLSM").postUpdate(GLSM_ON);
    console.log("GarageLightsProxy -> ON, GLSM -> " + GLSM_ON);
  }
});

rules.JSRule({
  name: "Garage Lights Commanded Off",
  triggers: [triggers.ItemStateChangeTrigger("GarageLightsProxy", undefined, "OFF")],
  execute: (event) => {
    items.getItem("GLSM").postUpdate(GLSM_OFF);
    console.log("GarageLightsProxy -> OFF, GLSM -> " + GLSM_OFF);
  }
});
