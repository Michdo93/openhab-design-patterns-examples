let until = null;

rules.JSRule({
  name: "Latched Rule",
  triggers: [triggers.ItemStateUpdateTrigger("MyItem")],
  execute: (event) => {
    const now = time.ZonedDateTime.now();
    if (until !== null && until.isAfter(now)) return; // Skip event if timer exists

    until = now.plusDays(1);

    // Regelcode ausfuehren
  }
});
