const commands = [];
let gateTimer = null;
let lastCommand = time.ZonedDateTime.now().minusSeconds(1);

function processQueue() {
  if (commands.length > 0) {
    const cmd = commands.shift();
    const results = actions.Exec.executeCommandLine(time.Duration.ofMillis(5000), cmd.split(" "));
    console.debug("433: " + results);
    lastCommand = time.ZonedDateTime.now();
  }

  const deltaMillis = time.Duration.between(lastCommand, time.ZonedDateTime.now()).toMillis();
  gateTimer.reschedule(time.ZonedDateTime.now().plusMillis(deltaMillis < 100 ? 100 - deltaMillis : 0));
}

rules.JSRule({
  name: "433MHz Controller",
  triggers: [triggers.ItemCommandTrigger("WirelessController")],
  execute: (event) => {
    commands.push(String(event.receivedCommand));

    if (gateTimer === null) {
      gateTimer = actions.ScriptExecution.createTimer(time.ZonedDateTime.now(), processQueue);
    }
  }
});

rules.JSRule({
  name: "Outlet A",
  triggers: [triggers.ItemCommandTrigger("Outlet_A")],
  execute: (event) => {
    if (event.receivedCommand === "ON") {
      items.getItem("WirelessController").sendCommand("433-send xxxxx 1 1");
    } else {
      items.getItem("WirelessController").sendCommand("433-send xxxxx 1 0");
    }
  }
});
