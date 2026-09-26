const GLSM_OFF = "0";
const GLSM_TIMED_ON = "2";
const GLSM_TIMED_BLINK = "3";

rules.JSRule({
  name: "GLSM - Garage Door Up Event Handler",
  triggers: [
    triggers.ItemStateChangeTrigger("LeftGarageDoor", undefined, "OPEN"),
    triggers.ItemStateChangeTrigger("RightGarageDoor", undefined, "OPEN")
  ],
  execute: (event) => {
    const sunset = items.getItem("Sun_Set").rawState;
    const afterSunset = sunset && time.toZDT(sunset).isBefore(time.ZonedDateTime.now());
    const state = items.getItem("GLSM").state;

    if (afterSunset && (state === GLSM_OFF || state === GLSM_TIMED_ON || state === GLSM_TIMED_BLINK)) {
      items.getItem("GLSM").postUpdate(GLSM_TIMED_ON);
      console.log("Door opened after sunset -> light on with timer");
    } else {
      console.log("Door opened, but no trigger (before sunset or light already permanently on)");
    }
  }
});
