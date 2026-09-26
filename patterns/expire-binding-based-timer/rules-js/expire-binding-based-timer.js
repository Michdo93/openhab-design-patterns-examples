rules.JSRule({
  name: "A rule that starts the timer",
  triggers: [triggers.ItemCommandTrigger("StartMyTimerTrigger", "ON")],
  execute: (event) => {
    // Arbeitsschritte ausführen

    if (items.getItem("MyTimer").state === "ON") {
      console.log("Timer is already active - restarting");
      // Aktion, falls Timer aktiv ist
    }

    // Timer abbrechen
    items.getItem("MyTimer").postUpdate("OFF");

    // Timer starten
    items.getItem("MyTimer").sendCommand("ON");
    console.log("MyTimer started (5 minutes)");
  }
});

rules.JSRule({
  name: "MyTimer expired",
  triggers: [triggers.ItemCommandTrigger("MyTimer", "OFF")],
  execute: (event) => {
    console.log("MyTimer expired - running expiry code");
    // Code, der nach Ablauf ausgeführt werden soll
  }
});
