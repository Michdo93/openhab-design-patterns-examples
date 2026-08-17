const { setDeferred, cancelDeferred } = require("./lib/deferred");

rules.JSRule({
  name: "Timer setzen",
  triggers: [triggers.GroupStateChangeTrigger("gDeferredAction")],
  execute: (event) => {
    const rawState = items.getItem(event.itemName).state;
    if (!event.itemName.endsWith("_Timer") || !rawState) return;

    const target = event.itemName.replace(/_Timer$/i, "");
    setDeferred(target, rawState);
    items.getItem(event.itemName).postUpdate("");
  }
});

rules.JSRule({
  name: "Timer entfernen",
  triggers: [triggers.GroupStateChangeTrigger("gDeferredAction")],
  execute: (event) => {
    cancelDeferred(event.itemName);
  }
});
