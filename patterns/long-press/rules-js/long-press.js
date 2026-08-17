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
      items.getItem("TargetLight").sendToggle();
    } else {
      // langer Druck
      items.getItem("TargetLight").sendCommand("INCREASE");
    }
    items.getItem("ButtonPressTime").postUpdate(pressDuration);
  }
});
