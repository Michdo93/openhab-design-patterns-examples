const retryTimers = new Map();
const retryCounts = new Map();

rules.JSRule({
  name: "Configurable Multi-Device Retry",
  triggers: [triggers.ItemStateChangeTrigger("RetryTrigger", undefined, "ON")],
  execute: (event) => {
    const maxRetries = parseInt(items.getItem("RetryMaxAttempts").state);
    const initialInterval = parseInt(items.getItem("RetryInitialInterval").state);
    const maxInterval = parseInt(items.getItem("RetryMaxInterval").state);
    const altAction = items.getItem("RetryAlternativeAction").state;

    const devices = items.getItem("RetryDevices").members.map((i) => i.name);

    devices.forEach((device) => {
      retryCounts.set(device, 0);

      const attempt = () => {
        try {
          if (items.getItem(device).state !== "NULL") {
            items.getItem(device).sendCommand("ON");
            console.log(device + " command sent successfully!");
            if (retryTimers.has(device)) retryTimers.get(device).cancel();
          } else {
            throw new Error("Device " + device + " is offline");
          }
        } catch (ex) {
          const count = retryCounts.get(device) + 1;
          retryCounts.set(device, count);
          console.warn(device + " attempt #" + count + " failed: " + ex.message);

          if (count < maxRetries) {
            const nextInterval = Math.min(initialInterval * Math.pow(2, count), maxInterval);
            console.log("Next attempt for " + device + " in " + nextInterval + " seconds");
            retryTimers.get(device).reschedule(time.ZonedDateTime.now().plusSeconds(nextInterval));
          } else {
            console.error(device + " max retries reached!");
            const message = altAction ? device + ": " + altAction : device + " could not be switched ON!";
            actions.NotificationAction.sendNotification("admin@example.com", message);
          }
        }
      };

      const t = actions.ScriptExecution.createTimer(time.ZonedDateTime.now(), attempt);
      retryTimers.set(device, t);
    });
  }
});
