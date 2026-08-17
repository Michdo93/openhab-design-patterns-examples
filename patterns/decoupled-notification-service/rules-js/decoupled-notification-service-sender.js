rules.JSRule({
  name: "Info Notification",
  triggers: [triggers.ItemStateChangeTrigger("SomeCondition", undefined, "ON")],
  execute: (event) => {
    items.getItem("VT_Notify_Info").postUpdate("Information: Zustand geaendert");
  }
});
