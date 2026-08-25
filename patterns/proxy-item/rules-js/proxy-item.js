rules.JSRule({
  name: "ProxySwitch erhielt Befehl",
  triggers: [triggers.ItemCommandTrigger("ProxySwitch")],
  execute: (event) => {
    const commandStr = String(event.receivedCommand);
    if (items.getItem("BoundSwitch").state !== commandStr) {
      items.getItem("BoundSwitch").sendCommand(event.receivedCommand);
      console.log("ProxySwitch -> BoundSwitch: " + commandStr);
    }
  }
});

rules.JSRule({
  name: "BoundSwitchUpdates erhielt Update",
  triggers: [triggers.ItemStateUpdateTrigger("BoundSwitchUpdates")],
  execute: (event) => {
    const stateStr = String(event.receivedState);
    if (items.getItem("ProxySwitch").state !== stateStr) {
      items.getItem("ProxySwitch").postUpdate(event.receivedState);
      console.log("BoundSwitchUpdates -> ProxySwitch: " + stateStr);
    }
  }
});
