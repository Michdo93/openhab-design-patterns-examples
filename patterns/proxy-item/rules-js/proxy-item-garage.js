rules.JSRule({
  name: "Garagentor Controller",
  triggers: [
    triggers.ItemCommandTrigger("Large_Garagedoor_Opener"),
    triggers.ItemCommandTrigger("Small_Garagedoor_Opener")
  ],
  execute: (event) => {
    if (items.getItem("GarageControllerComputer").state !== "ON" ||
        items.getItem("GarageControllerService").state !== "ON") {
      items.getItem("AlertItem").sendCommand("Garagentor-Controller offline!");
    }
    items.getItem(event.itemName + "_Linked").sendCommand(event.receivedCommand);
    console.log(event.itemName + " -> " + event.itemName + "_Linked: " + event.receivedCommand);
  }
});
