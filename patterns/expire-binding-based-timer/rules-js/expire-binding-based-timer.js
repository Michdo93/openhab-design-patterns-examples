rules.JSRule({
  name: "Eine Regel, die den Timer startet",
  triggers: [triggers.ItemCommandTrigger("StartMyTimerTrigger", "ON")],
  execute: (event) => {
    // Arbeitsschritte ausfuehren

    if (items.getItem("MyTimer").state === "ON") {
      // Aktion, falls Timer aktiv ist
    }

    // Timer abbrechen
    items.getItem("MyTimer").postUpdate("OFF");

    // Timer starten
    items.getItem("MyTimer").sendCommand("ON");
  }
});

rules.JSRule({
  name: "MyTimer abgelaufen",
  triggers: [triggers.ItemCommandTrigger("MyTimer", "OFF")],
  execute: (event) => {
    // Code, der nach Ablauf ausgefuehrt werden soll
  }
});
