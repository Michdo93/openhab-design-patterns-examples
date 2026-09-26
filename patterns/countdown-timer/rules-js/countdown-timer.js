rules.JSRule({
  name: "Countdown management",
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
  name: "Start 6 minutes",
  triggers: [triggers.ItemCommandTrigger("test6")],
  execute: (event) => { items.getItem("myCounter").sendCommand(6); }
});

rules.JSRule({
  name: "Start 3 minutes",
  triggers: [triggers.ItemCommandTrigger("test3")],
  execute: (event) => { items.getItem("myCounter").sendCommand(3); }
});

rules.JSRule({
  name: "Set to 2 minutes",
  triggers: [triggers.ItemCommandTrigger("test2")],
  execute: (event) => { items.getItem("myCounter").sendCommand(-2); }
});

rules.JSRule({
  name: "Cancel countdown",
  triggers: [triggers.ItemCommandTrigger("testabort")],
  execute: (event) => { items.getItem("myCounter").sendCommand(0); }
});
