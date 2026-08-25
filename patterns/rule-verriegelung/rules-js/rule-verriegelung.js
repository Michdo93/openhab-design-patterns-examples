let until = null;

rules.JSRule({
  name: "Latched Rule",
  triggers: [triggers.ItemStateUpdateTrigger("MyItem")],
  execute: (event) => {
    const now = time.ZonedDateTime.now();
    if (until !== null && until.isAfter(now)) {
      console.log("Event ignoriert, gesperrt bis " + until.toString());
      return; // Skip event if timer exists
    }

    until = now.plusDays(1);
    console.log("Regelcode ausgefuehrt, gesperrt bis " + until.toString());

    // Regelcode ausfuehren
  }
});
