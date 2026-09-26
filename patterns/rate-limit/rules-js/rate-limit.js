rules.JSRule({
  name: "Rate limit example",
  triggers: [triggers.ItemCommandTrigger("RateLimitTrigger", "ON")],
  execute: (event) => {
    const lastAction = cache.private.get("LastAction", () => time.ZonedDateTime.now().minusDays(1));

    if (lastAction.isBefore(time.ZonedDateTime.now().minusHours(24))) {
      console.log("Rate-limited action");
      cache.private.put("LastAction", time.ZonedDateTime.now());
    } else {
      console.log("Event ignored, lockout period still running");
    }
  }
});
