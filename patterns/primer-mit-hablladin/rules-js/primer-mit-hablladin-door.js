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
    const afterSunset = sunset && time.ZonedDateTime.parse(String(sunset)).isBefore(time.ZonedDateTime.now());
    const state = items.getItem("GLSM").state;

    if (afterSunset && (state === GLSM_OFF || state === GLSM_TIMED_ON || state === GLSM_TIMED_BLINK)) {
      items.getItem("GLSM").postUpdate(GLSM_TIMED_ON);
      console.log("Tor geoeffnet nach Sonnenuntergang -> Licht mit Timer an");
    } else {
      console.log("Tor geoeffnet, aber kein Trigger (vor Sonnenuntergang oder Licht bereits dauerhaft an)");
    }
  }
});
