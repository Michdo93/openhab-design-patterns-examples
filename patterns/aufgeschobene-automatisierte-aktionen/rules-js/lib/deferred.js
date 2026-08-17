const timers = new Map();

const TIME_OFFSET = /^(?:\+((?:\d+[hms])+))->(.*)$/i;
const TIME_SPECIFIC = /^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})->(.*)$/;

function parseOffsetToSeconds(offset) {
  const re = /(\d+)([hms])/gi;
  let total = 0;
  let m;
  while ((m = re.exec(offset)) !== null) {
    const value = parseInt(m[1]);
    const unit = m[2].toLowerCase();
    if (unit === "h") total += value * 3600;
    else if (unit === "m") total += value * 60;
    else total += value;
  }
  return total;
}

function setDeferred(target, rawState) {
  let triggerTime;
  let command;

  let match = TIME_OFFSET.exec(rawState);
  if (match) {
    triggerTime = time.ZonedDateTime.now().plusSeconds(parseOffsetToSeconds(match[1]));
    command = match[2];
  } else {
    match = TIME_SPECIFIC.exec(rawState);
    if (!match) throw new Error("Ungueltiges Timerformat [" + rawState + "]");
    triggerTime = time.ZonedDateTime.parse(match[1] + time.ZonedDateTime.now().offset().id());
    command = match[2];
  }

  if (triggerTime.isBefore(time.ZonedDateTime.now())) {
    throw new Error("Zielzeit liegt in der Vergangenheit");
  }

  cancelDeferred(target);

  const t = actions.ScriptExecution.createTimer(triggerTime, () => {
    console.log("Ausfuehren verzoegerter Aktion " + command + " auf " + target);
    timers.delete(target);
    items.getItem(target).sendCommand(command);
  });
  timers.set(target, t);
}

function cancelDeferred(target) {
  if (timers.has(target)) {
    timers.get(target).cancel();
    timers.delete(target);
  }
}

module.exports = { setDeferred, cancelDeferred };
