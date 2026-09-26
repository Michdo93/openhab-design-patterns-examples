rules.JSRule({
  name: "Button pressed (with fallback)",
  triggers: [triggers.ItemStateChangeTrigger("ButtonState", "OFF", "ON")],
  execute: (event) => {
    actions.ScriptExecution.createTimer(time.ZonedDateTime.now().plusSeconds(5), () => {
      if (items.getItem("ButtonState").state === "ON") {
        console.log("Fallback: no OFF signal received, resetting ButtonState manually");
        items.getItem("ButtonState").postUpdate("OFF");
      }
    });
  }
});
