const MAX_RETRIES = 3;
const RETRY_INTERVAL = 10; // Sekunden

rules.JSRule({
  name: "Graceful Retry LightSwitch",
  triggers: [triggers.ItemStateChangeTrigger("SomeTrigger", undefined, "ON")],
  execute: (event) => {
    let retryCount = 0;
    let retryTimer = null;

    const attempt = () => {
      try {
        items.getItem("LightSwitch").sendCommand("ON");
        console.log("Command erfolgreich gesendet!");
        if (retryTimer !== null) retryTimer.cancel();
      } catch (e) {
        retryCount++;
        console.warn("Fehler beim Senden, Versuch #" + retryCount);
        if (retryCount < MAX_RETRIES) {
          retryTimer.reschedule(time.ZonedDateTime.now().plusSeconds(RETRY_INTERVAL));
        } else {
          console.error("Maximale Anzahl an Versuchen erreicht!");
          try {
            items.getItem("NotificationItem").postUpdate("LightSwitch konnte nicht eingeschaltet werden");
          } catch (notifyItemEx) {
            console.warn("Konnte NotificationItem nicht aktualisieren: " + notifyItemEx.message);
          }
          try {
            if (actions.NotificationAction) {
              actions.NotificationAction.sendNotification("admin@example.com", "LightSwitch konnte nicht eingeschaltet werden");
            }
          } catch (notifyEx) {
            console.warn("Cloud-Benachrichtigung nicht verfuegbar: " + notifyEx.message);
          }
        }
      }
    };

    retryTimer = actions.ScriptExecution.createTimer(time.ZonedDateTime.now(), attempt);
  }
});
