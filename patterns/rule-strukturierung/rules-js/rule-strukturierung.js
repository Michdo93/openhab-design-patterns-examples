rules.JSRule({
  name: "1-2-3 Rule Structure",
  triggers: [
    triggers.ItemStateChangeTrigger("Foo"),
    triggers.ItemStateChangeTrigger("Bar"),
    triggers.ItemStateChangeTrigger("Baz")
  ],
  execute: (event) => {
    const foo = items.getItem("Foo").state;
    const bar = items.getItem("Bar").state;
    const baz = items.getItem("Baz").state;

    // 1. Pruefen, ob Regel laufen muss
    if (foo === "NULL" || bar === "NULL" || baz === "NULL") {
      console.warn("One of the Items is NULL");
      return;
    }

    // 2. Berechnen
    const onCount = [foo, bar, baz].filter((s) => s === "ON").length;
    const newState = onCount >= 2 ? "ON" : "OFF";

    // 3. Ausfuehren
    items.getItem("Buzz").sendCommand(newState);
  }
});
