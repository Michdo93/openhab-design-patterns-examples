rules.JSRule({
  name: "Group Approach",
  triggers: [triggers.GroupStateChangeTrigger("MyGroup")],
  execute: (event) => {
    const members = items.getItem("MyGroup").members;
    if (members.some((i) => i.state === "NULL")) {
      console.warn("One of the Items is NULL");
      return;
    }
    const sum = members.filter((i) => i.state === "ON").length;
    items.getItem("Buzz").sendCommand(sum >= 2 ? "ON" : "OFF");
  }
});
