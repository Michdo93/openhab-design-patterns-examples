rules.JSRule({
  name: "Button gedrueckt (mit Fallback)",
  triggers: [triggers.ItemStateChangeTrigger("ButtonState", "OFF", "ON")],
  execute: (event) => {
    actions.ScriptExecution.createTimer(time.ZonedDateTime.now().plusSeconds(5), () => {
      if (items.getItem("ButtonState").state === "ON") {
        console.log("Fallback: kein OFF-Signal erhalten, setze ButtonState manuell zurueck");
        items.getItem("ButtonState").postUpdate("OFF");
      }
    });
  }
});
