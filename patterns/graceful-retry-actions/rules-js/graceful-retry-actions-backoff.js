const MAX_RETRIES_BACKOFF = 5;
const MAX_INTERVAL = 60;

rules.JSRule({
  name: "Graceful Retry LightSwitch with Backoff",
  triggers: [triggers.ItemStateChangeTrigger("SomeTrigger", undefined, "ON")],
  execute: (event) => {
    let retryCount = 0;
    let retryInterval = 5;
    let retryTimer = null;

    const attempt = () => {
      try {
        items.getItem("LightSwitch").sendCommand("ON");
        console.log("Command erfolgreich gesendet!");
        if (retryTimer !== null) retryTimer.cancel();
      } catch (e) {
        retryCount++;
        console.warn("Fehlversuch #" + retryCount);
        if (retryCount < MAX_RETRIES_BACKOFF) {
          retryInterval = Math.min(retryInterval * 2, MAX_INTERVAL);
          console.log("Naechster Versuch in " + retryInterval + " Sekunden");
          retryTimer.reschedule(time.ZonedDateTime.now().plusSeconds(retryInterval));
        } else {
          console.error("Maximale Anzahl an Versuchen erreicht!");
          actions.NotificationAction.sendNotification("admin@example.com", "LightSwitch konnte nicht eingeschaltet werden");
        }
      }
    };

    retryTimer = actions.ScriptExecution.createTimer(time.ZonedDateTime.now(), attempt);
  }
});
