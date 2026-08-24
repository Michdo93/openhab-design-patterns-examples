rules.JSRule({
  name: "ProxySwitch erhielt Befehl",
  triggers: [triggers.ItemCommandTrigger("ProxySwitch")],
  execute: (event) => {
    if (items.getItem("BoundSwitch").state !== String(event.receivedCommand)) {
      items.getItem("BoundSwitch").sendCommand(event.receivedCommand);
    }
  }
});

rules.JSRule({
  name: "BoundSwitchUpdates erhielt Update",
  triggers: [triggers.ItemStateUpdateTrigger("BoundSwitchUpdates")],
  execute: (event) => {
    if (items.getItem("ProxySwitch").state !== String(event.receivedState)) {
      items.getItem("ProxySwitch").postUpdate(event.receivedState);
    }
  }
});
