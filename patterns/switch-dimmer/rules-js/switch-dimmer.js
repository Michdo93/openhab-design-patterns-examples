const timers = new Map();
const timestamps = new Map();

function switchPressed(id) {
  timestamps.set(id, time.ZonedDateTime.now());
  items.getItem(id).sendCommand("ON");

  const t = actions.ScriptExecution.createTimer(time.ZonedDateTime.now().plusMillis(500), () => {
    items.getItem(id + "LongPress").sendCommand("ON");
    items.getItem(id + "LongPress").sendCommand("OFF");
    const pressedAt = timestamps.get(id);
    if (pressedAt && time.ZonedDateTime.now().isBefore(pressedAt.plusSeconds(5))) {
      timers.get(id).reschedule(time.ZonedDateTime.now().plusMillis(500));
    }
  });
  timers.set(id, t);
}

function switchReleased(id) {
  if (timers.has(id)) {
    timers.get(id).cancel();
    timers.delete(id);
  }
  const pressed = timestamps.get(id);
  timestamps.delete(id);

  if (pressed && time.ZonedDateTime.now().isBefore(pressed.plusMillis(500))) {
    items.getItem(id + "ShortPress").sendCommand("ON");
    items.getItem(id + "ShortPress").sendCommand("OFF");
  }

  items.getItem(id).sendCommand("OFF");
}

rules.JSRule({
  name: "Switch1Events",
  triggers: [triggers.ChannelEventTrigger("enocean:rockerSwitch:xxxxxxxx:xxxxxxxx:rockerswitchA")],
  execute: (event) => {
    switch (event.receivedEvent) {
      case "DIR1_PRESSED":  switchPressed("MySwitch1Up"); break;
      case "DIR1_RELEASED": switchReleased("MySwitch1Up"); break;
      case "DIR2_PRESSED":  switchPressed("MySwitch1Down"); break;
      case "DIR2_RELEASED": switchReleased("MySwitch1Down"); break;
    }
  }
});
