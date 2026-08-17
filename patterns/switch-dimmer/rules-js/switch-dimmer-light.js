let myColorLightCommand = "INCREASE";

rules.JSRule({
  name: "MyColorLight_OnOff",
  triggers: [triggers.ItemCommandTrigger("MySwitch1UpShortPress", "ON")],
  execute: (event) => {
    const brightness = items.getItem("MyColorLight").state; // HSB-Helligkeit
    if (parseFloat(brightness.split(",")[2]) === 0) {
      myColorLightCommand = "INCREASE";
      items.getItem("MyColorLight").sendCommand("ON");
    } else {
      myColorLightCommand = "DECREASE";
      items.getItem("MyColorLight").sendCommand("OFF");
    }
  }
});

rules.JSRule({
  name: "MyColorLight_Dimmer",
  triggers: [triggers.ItemCommandTrigger("MySwitch1UpLongPress", "ON")],
  execute: (event) => {
    items.getItem("MyColorLight").sendCommand(myColorLightCommand);
  }
});
