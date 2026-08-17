rules.JSRule({
  name: "Button gedrueckt (mit Fallback)",
  triggers: [triggers.ItemStateChangeTrigger("ButtonState", "OFF", "ON")],
  execute: (event) => {
    pressStart = time.ZonedDateTime.now();
    actions.ScriptExecution.createTimer(time.ZonedDateTime.now().plusSeconds(5), () => {
      if (items.getItem("ButtonState").state === "ON") {
        items.getItem("ButtonState").postUpdate("OFF");
      }
    });
  }
});
