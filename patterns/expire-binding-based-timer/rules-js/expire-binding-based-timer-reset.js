rules.JSRule({
  name: "Restart expire timers",
  description: "Reactivates all expire timers after system start",
  triggers: [triggers.SystemStartlevelTrigger(100)],
  execute: (event) => {
    console.log("Restarting expire timers");
    items.getItem("gResetExpire").members.forEach((timer) => {
      timer.sendCommand(timer.state);
    });
  }
});
