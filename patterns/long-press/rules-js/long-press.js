let pressStart = null;

rules.JSRule({
  name: "Button gedrueckt",
  triggers: [triggers.ItemStateChangeTrigger("ButtonState", "OFF", "ON")],
  execute: (event) => {
    pressStart = time.ZonedDateTime.now();
  }
});

rules.JSRule({
  name: "Button losgelassen",
  triggers: [triggers.ItemStateChangeTrigger("ButtonState", "ON", "OFF")],
  execute: (event) => {
    if (pressStart === null) return;

    const pressDuration = time.Duration.between(pressStart, time.ZonedDateTime.now()).toMillis();

    if (pressDuration < 500) {
      // kurzer Druck
      const newState = items.getItem("TargetLight").state === "ON" ? "OFF" : "ON";
      items.getItem("TargetLight").sendCommand(newState);
      console.log("Kurzer Druck (" + pressDuration + "ms) -> Toggle (" + newState + ")");
    } else {
      // langer Druck
      items.getItem("TargetLight").sendCommand("INCREASE");
      console.log("Langer Druck (" + pressDuration + "ms) -> Dimmen");
    }
    items.getItem("ButtonPressTime").postUpdate(pressDuration);
  }
});
