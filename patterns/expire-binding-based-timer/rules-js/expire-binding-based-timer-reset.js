rules.JSRule({
  name: "Expire-Timer neu starten",
  description: "Aktiviert alle Expire-Timer nach Systemstart",
  triggers: [triggers.SystemStartlevelTrigger(100)],
  execute: (event) => {
    console.log("Expire-Timer werden neu gestartet");
    items.getItem("gResetExpire").members.forEach((timer) => {
      timer.sendCommand(timer.state);
    });
  }
});
