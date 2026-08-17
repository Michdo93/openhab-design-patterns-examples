rules.JSRule({
  name: "Countdown-Verwaltung",
  triggers: [triggers.ItemCommandTrigger("myCounter")],
  execute: (event) => {
    const cmmd = parseInt(event.receivedCommand);
    let count = 0;
    const state = items.getItem("myCounter").rawState;
    if (state != null && state.toString() !== "NULL") {
      count = parseInt(items.getItem("myCounter").state);
    }

    if (cmmd === -1 && count > 0) {
      if (count === 1) {
        items.getItem("testLamp").sendCommand("OFF");
      }
      items.getItem("myCounter").postUpdate(count - 1);
    } else if (cmmd >= count || cmmd < -1) {
      let newCount = cmmd < -1 ? -cmmd : cmmd;
      items.getItem("myCounter").postUpdate(newCount);
      if (items.getItem("testLamp").state !== "ON") {
        items.getItem("testLamp").sendCommand("ON");
      }
    } else if (cmmd === 0) {
      items.getItem("myCounter").postUpdate(0);
      items.getItem("testLamp").sendCommand("OFF");
    }
  }
});

rules.JSRule({
  name: "6 Minuten starten",
  triggers: [triggers.ItemCommandTrigger("test6")],
  execute: (event) => { items.getItem("myCounter").sendCommand(6); }
});

rules.JSRule({
  name: "3 Minuten starten",
  triggers: [triggers.ItemCommandTrigger("test3")],
  execute: (event) => { items.getItem("myCounter").sendCommand(3); }
});

rules.JSRule({
  name: "auf 2 Minuten setzen",
  triggers: [triggers.ItemCommandTrigger("test2")],
  execute: (event) => { items.getItem("myCounter").sendCommand(-2); }
});

rules.JSRule({
  name: "Countdown abbrechen",
  triggers: [triggers.ItemCommandTrigger("testabort")],
  execute: (event) => { items.getItem("myCounter").sendCommand(0); }
});
