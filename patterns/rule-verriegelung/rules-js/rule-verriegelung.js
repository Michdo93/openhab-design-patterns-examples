let until = null;

rules.JSRule({
  name: "Latched Rule",
  triggers: [triggers.ItemStateUpdateTrigger("MyItem")],
  execute: (event) => {
    const now = time.ZonedDateTime.now();
    if (until !== null && until.isAfter(now)) {
      console.log("Event ignored, locked until " + until.toString());
      return; // Ereignis überspringen, solange die Sperre aktiv ist
    }

    until = now.plusDays(1);
    console.log("Rule code executed, locked until " + until.toString());

    // Regelcode ausführen
  }
});
