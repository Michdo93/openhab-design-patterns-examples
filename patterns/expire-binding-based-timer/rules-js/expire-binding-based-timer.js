rules.JSRule({
  name: "Eine Regel, die den Timer startet",
  triggers: [triggers.ItemCommandTrigger("StartMyTimerTrigger", "ON")],
  execute: (event) => {
    // Arbeitsschritte ausfuehren

    if (items.getItem("MyTimer").state === "ON") {
      console.log("Timer ist bereits aktiv - wird neu gestartet");
      // Aktion, falls Timer aktiv ist
    }

    // Timer abbrechen
    items.getItem("MyTimer").postUpdate("OFF");

    // Timer starten
    items.getItem("MyTimer").sendCommand("ON");
    console.log("MyTimer gestartet (5 Minuten)");
  }
});

rules.JSRule({
  name: "MyTimer abgelaufen",
  triggers: [triggers.ItemCommandTrigger("MyTimer", "OFF")],
  execute: (event) => {
    console.log("MyTimer abgelaufen - Code nach Ablauf wird ausgefuehrt");
    // Code, der nach Ablauf ausgefuehrt werden soll
  }
});
