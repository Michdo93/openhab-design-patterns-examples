const GLSM_OFF = "0";
const GLSM_ON = "1";
const GLSM_TIMED_ON = "2";
const GLSM_TIMED_BLINK = "3";

let glsmTimer = null;

rules.JSRule({
  name: "GLSM - Garage Lights State Machine Events Handler",
  triggers: [triggers.ItemStateUpdateTrigger("GLSM")],
  execute: (event) => {
    const state = items.getItem("GLSM").state;

    if (state === "NULL" || state === "UNDEF") {
      items.getItem("GarageLights").sendCommand("OFF");
      items.getItem("GLSM").postUpdate(GLSM_OFF);
    } else if (state === GLSM_OFF) {
      items.getItem("GarageLights").sendCommand("OFF");
      if (glsmTimer !== null) { glsmTimer.cancel(); glsmTimer = null; }
    } else if (state === GLSM_ON) {
      items.getItem("GarageLights").sendCommand("ON");
      if (glsmTimer !== null) { glsmTimer.cancel(); glsmTimer = null; }
    } else if (state === GLSM_TIMED_ON) {
      items.getItem("GarageLights").sendCommand("ON");
      glsmTimer = actions.ScriptExecution.createTimer(
        time.ZonedDateTime.now().plusMinutes(5),
        () => items.getItem("GLSM").postUpdate(GLSM_TIMED_BLINK)
      );
    } else if (state === GLSM_TIMED_BLINK) {
      items.getItem("GarageLights").sendCommand("OFF");
      items.getItem("GarageLights").sendCommand("ON");
      glsmTimer = actions.ScriptExecution.createTimer(
        time.ZonedDateTime.now().plusMinutes(1),
        () => items.getItem("GLSM").postUpdate(GLSM_OFF)
      );
    }
  }
});
